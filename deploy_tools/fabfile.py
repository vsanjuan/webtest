from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL ='https://github.com/vsanjuan/webtest.git'
URL = '54.171.128.243'
folder_web = "testweb"
user = "ubuntu"

def deploy():
  site_folder = '/home/%s/sites/%s' % (user, folder_web)
  source_folder = site_folder + '/source'
  _server()
  # _create_directory_structure_if_necessary(site_folder)
  _get_lastest_source(source_folder)
  # _update_settings(source_folder, env.host)
  # _update_virtualenv(source_folder)
  # _update_static_files(source_folder)
  # _update_database(source_folder)

def _server() :
  """This pushes to the EC2 instance defined below"""
  # The Elastic IP to your server
  env.host_string = URL
  # your user on that system
  env.user = user
  # Assumes that your *.pem key is in the same directory as your fabfile.py
  env.key_filename = 'C:/Users/Salvador/.ssh/bitnami-hosting.pem'

def _create_directory_structure_if_necessary(site_folder):
  for subfolder in ('database', 'static', 'virtualenv', 'source'):
    run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_lastest_source(source_folder):
  if exists(source_folder + '/.git'):
    run('cd %s && git fetch' % (source_folder, ))
  else:
    run('git clone %s %s' % (REPO_URL, source_folder))
  current_commit = local("git log -n 1 --format=%H", capture=True)
  run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name):
  setting_path = source_folder + '/testweb/settings.py'
  sed(setting_path, "DEBUG = True", "DEBUG = False")
  sed(setting_path,
      'ALLOWED_HOSTS =.+$',
      'ALLOWED_HOSTS = ["%s"]' % (URL,)
  )
  secret_key_file = source_folder + '/testweb/secret_key.py'
  if not exists(secret_key_file):
    chars= 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
    append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
  append(setting_path, "\nfrom .secret_key import SECRET_KEY")

def _update_virtualenv(source_folder):
  virtualenv_folder = source_folder + '/../virtualenv'
  if not exists(virtualenv_folder + '/bin/pip'):
    # there is a problem with the requirements.txt due to the encoding
    run('virtualenv --python=python3 %s' % (virtualenv_folder,))
  run('%s/bin/pip install -r %s/requirements.txt' % (
            virtualenv_folder, source_folder
  ))

def _update_static_files(source_folder):
  run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (
      source_folder
  ))

def _update_database(source_folder):
  run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
      source_folder
  ))
