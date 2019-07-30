#!/usr/bin/env python
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from pen_apple import celery, create_app, db, models

wtf_app = create_app(os.getenv('FLASK_CONFIG') or 'default')
worker = celery
manager = Manager(wtf_app)
migrate = Migrate(wtf_app, db)
manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    context = dict(app=wtf_app, db=db)
    context.update(vars(models))
    return context


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def cov():
    import unittest
    import coverage
    import os
    cov = coverage.coverage(
        branch=True,
        include='pen_apple/*')
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()


if __name__ == '__main__':
    manager.run()
