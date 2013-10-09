from fabric.api import run, sudo, local, cd, env

env.hosts = ['oolong.thraxil.org', 'maru.thraxil.org']
env.user = 'anders'

def restart_gunicorn():
    sudo("restart skinflint")

def prepare_deploy():
    local("./manage.py test")

def deploy():
    code_dir = "/var/www/skinflint/skinflint"
    with cd(code_dir):
        run("git pull origin master")
        run("./bootstrap.py")
        run("./manage.py migrate")
    restart_gunicorn()