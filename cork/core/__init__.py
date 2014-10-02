def _register(app, manager):
    from cork.core.commands import TestCommand
    manager.add_command('test', TestCommand)
