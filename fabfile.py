import os
from fabric.api import run, cd
from fabric.contrib.project import rsync_project
from fabric.contrib.files import exists

__author__ = 'nampnq'

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

EXCLUDE_PATTERNS = [
    '*.rst', '*.pyc', '*~', '*.swp', '.git/', 'env/', '.idea', 'gunicorn.pid', 'edelivery.db'
]


def deploy():

    rsync_project(local_dir=ROOT_PATH + '/',
                  remote_dir='/srv/eDelivery',
                  delete=True,
                  exclude=EXCLUDE_PATTERNS,
                  extra_opts='--chmod=Du=rwx,Dgo=rx,Fu=rw,Fgo=r')
    with cd('/srv/eDelivery'):
        if exists('gunicorn.pid'):
            run("kill `cat gunicorn.pid`")
            # run('dtach -n `mktemp -u /tmp/dtach.XXXX` `nohup env/bin/gunicorn wsgi:app -b localhost:9992 -p gunicorn.pid &`')