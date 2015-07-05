#!/usr/bin/env python
from flask.ext.script import Manager
from api.app import create_app
from api.models import db

manager = Manager(create_app)


@manager.command
def createdb():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()


@manager.command
def test():
    from subprocess import call
    call(['nosetests', '-v',
          '--with-coverage', '--cover-package=api', '--cover-branches',
          '--cover-erase', '--cover-html', '--cover-html-dir=cover'])


if __name__ == '__main__':
    manager.run()

