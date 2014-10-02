from flask.ext.script import Command, Option
from flask import current_app
from cork.utils import get_module, get_module_path
import pytest


class TestCommand(Command):
    option_list = (
        Option('module', nargs='?', help='a module to test'),
    )

    def run(self, module=None):
        modules = []
        if module is not None:
            modules = [module]
        else:
            modules = current_app.config['INSTALLED_APPS']

        test_modules = []

        current_app.db.create_all()

        for module in modules:
            try:
                get_module('%s.tests' % module)
                test_modules.append('%s/tests' % get_module_path(module))
            except ImportError:
                pass

        #cmd = '--cov-report html --cov .'
        #cmd += ' '.join(['--cov %s' % test_module.replace('/tests', '') for test_module in test_modules])
        cmd = ' '.join(test_modules)

        pytest.main(cmd)

        current_app.db.drop_all()
