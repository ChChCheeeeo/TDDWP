from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

#REPO_URL = 'https://github.com/hjwp/book-example.git'
REPO_URL = 'https://github.com/ChChCheeeeo/TDDWP.git'
def deploy():
    # env.host will contain the address of the server we've specified at the
    # command line, eg, superlists.ottg.eu
    # tmpdomain-staging.tmpdomain.xyz
    # tmpdomain.xyz
    # env.user will contain the username you're using to log in to the server
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    # build directory structure, in a way that doesn’t fall down
    # if it already exists
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        # fabric command - run this shell command on the server
        run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
    #  look for the .git hidden folder to check whether the repo has
    # already been cloned in that folder. 
    if exists(source_folder + '/.git'):
        # Fabric doesn’t have any state, so it doesn’t remember what
        # directory you’re in from one run to the next.
        # pull down all the latest commits
        run('cd %s && git fetch' % (source_folder,))
    else:
        # Alternatively use git clone with the repo URL to bring down
        # a fresh source tree
        run('git clone %s %s' % (REPO_URL, source_folder))
    # Fabric’s local command runs a command on your local machine—it’s
    # just a wrapper around subprocess.Popen really, but it’s quite
    # convenient. Here we capture the output from that git log
    # invocation to get the hash of the current commit that’s in your
    # local tree. That means the server will end up with whatever code
    # is currently checked out on your machine (as long as you’ve pushed
    # it up to the server). 
    current_commit = local("git log -n 1 --format=%H", capture=True)
    # reset --hard to that commit, which will blow away any current
    # changes in the server’s code directory. 
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name):
    # update the settings file, to set the ALLOWED_HOSTS and DEBUG,
    # and to create a new secret key
    settings_path = source_folder + '/superlists_project/base.py'#settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,)
    )
    secret_key_file = source_folder + '/superlists_project/secret_key.py'
    # It’s good practice to make sure the secret key on the server
    # is different from the one in your (possibly public) source code
    # repo. This code will generate a new key to import into settings,
    # if there isn’t one there already (once you have a secret key, it
    # should stay the same between deploys). 
    if not exists(secret_key_file):  #3
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    # 
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    # decided not to use venv_tdd_droplet_production as I dont know how it get
    # it to run virtualenwrapper's workon command
    source_folder = source_folder + '/requirements'
    # create or update the virtualenv
    virtualenv_folder = source_folder + '/../virtualenv'
    # look inside the virtualenv folder for the pip executable as a way of
    # checking whether it already exists
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/base.txt' % ( #requirements.txt' % (
            virtualenv_folder, source_folder
    ))

def _update_static_files(source_folder):
    # Updating static files is a single command
    # We use the virtualenv binaries folder whenever we need to run a Django
    # manage.py command, to make sure we get the virtualenv version of Django,
    # not the system one.
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % ( # 1
        source_folder,
    ))

def _update_database(source_folder):
    #  update the database with manage.py migrate
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
        source_folder,
    ))