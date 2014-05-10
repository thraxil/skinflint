from fabric.api import run, sudo, local, cd, env

env.hosts = ['orlando.thraxil.org']
nginx_hosts = ['lolrus.thraxil.org']
env.user = 'anders'
env.forward_agent = True

def restart_gunicorn():
    sudo("restart skinflint")

def prepare_deploy():
    local("make test")

def deploy():
    code_dir = "/var/www/skinflint/skinflint"
    with cd(code_dir):
        run("git pull origin master")
        run("make migrate")
        run("make collectstatic")
        for n in nginx_hosts:
            run(("rsync -avp --delete media/ "
                 "%s:/var/www/skinflint/skinflint/media/") % n)

    restart_gunicorn()
