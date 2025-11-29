from fabric.api import cd, run, local, sudo
from fabric.contrib.files import exists

REPO_URL = 'https://github.com/orichcasperkevin/church-is-frontend.git'


def deploy():
    site_folder = f'/home/nanoafrika/church-is-frontend'
    run(f'mkdir  -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_packages()
        _set_up_nginx()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git init')
        run(f'git remote add origin {REPO_URL}')
        run('git fetch')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')


def _update_packages():
    run('/home/nanoafrika/.nvm/versions/node/v8.11.1/bin/npm install')
    run(f'/home/nanoafrika/.nvm/versions/node/v8.11.1/bin/npm run build')


def _set_up_nginx():
    if not exists('/etc/nginx/sites-available/church_is_frontend'):
        sudo('cp nginx.template.conf /etc/nginx/sites-available/church_is_frontend')
        sudo('ln -s /etc/nginx/sites-available/church_is_frontend /etc/nginx/sites-enabled/church_is_frontend')
        sudo('service nginx restart')