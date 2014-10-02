from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.migrate import init as fminit
from flask.ext.migrate import migrate as fmmigrate
from flask.ext.migrate import upgrade as fmupgrade
from flask.ext.migrate import downgrade as fmdowngrade
from cork.utils import get_module_path
from cork.utils import get_app_module
from cork.utils import get_installed_modules
from flask import current_app
import os
import logging


logger = logging.getLogger(__name__)


@MigrateCommand.option('module', help='app module')
def init(directory, module):
    return fminit(directory='%s/migrations' % get_module_path(module))


@MigrateCommand.option('module', help='app module')
def migrate(module, *args, **kwargs):
    kwargs['directory'] = '%s/migrations' % get_module_path(module)
    return fmmigrate(**kwargs)


@MigrateCommand.option('module', nargs='?', help='app module')
def upgrade(module, *args, **kwargs):
    if module:
        kwargs['directory'] = '%s/migrations' % get_module_path(module)
        return fmupgrade(**kwargs)
    else:
        for module in get_installed_modules(current_app):
            if os.path.exists('%s/migrations' % get_module_path(module)):
                logger.debug('Migrating %s' % module)
                kwargs['directory'] = '%s/migrations' % get_module_path(module)
                fmupgrade(**kwargs)


@MigrateCommand.option('module', help='app module')
def downgrade(module, *args, **kwargs):
    kwargs['directory'] = '%s/migrations' % get_module_path(module)
    return fmdowngrade(**kwargs)


MigrateCommand._commands['init'].run = init
MigrateCommand._commands['migrate'].run = migrate
MigrateCommand._commands['upgrade'].run = upgrade
MigrateCommand._commands['downgrade'].run = downgrade


class BasicModelMixin(object):
    def __init__(self, *args, **kwargs):
        for attrname, attrvalue in kwargs.iteritems():
            setattr(self, attrname, attrvalue)


def _register(manager, app):
    migrate = Migrate(app, app.db)
    manager.add_command('db', MigrateCommand)
