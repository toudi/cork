import os
from importlib import import_module
from logging import getLogger
logger = getLogger(__name__)


def get_app_module():
    return import_module(os.environ.get('FLASK_APP', 'app'))


def get_module_path(module):
    if type(module) is str:
        module = import_module(module)
    return os.path.dirname(module.__file__)


def get_module(module):
    return import_module(module)


def get_installed_modules(app):
    for module in app.config['MODULES']:
        _mod = import_module(module)
        yield _mod


def autodiscover(**kwargs):
    if 'app' in kwargs:
        app = kwargs['app']
    elif 'manager' in kwargs:
        app = kwargs['manager'].app
    for module in get_installed_modules(app):
        if hasattr(module, '_register'):
            logger.debug('registering %r', module)
            module._register(**kwargs)
