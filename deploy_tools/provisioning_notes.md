Provisioning a new site =======================
## Required packages:
* nginx
* Python 3
* Git
* pip
* virtualenv

eg, on Ubuntu:
    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

## Nginx Virtual Host config
* see nginx.template.conf
* replace SITENAME with, eg, staging.my-domain.com
## Upstart Job
* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, staging.my-domain.com
## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
        └── SITENAME
                  ├── database
                  ├── source
                  ├── static
                  └── virtualenv We can do a commit for those:

$ git add deploy_tools
$ git status # see three new files
$ git commit -m "Notes and template config files for provisioning" Our source tree will now look something like this:
$ tree -I __pycache__
.
├── deploy_tools
│   ├── gunicorn-upstart.template.conf
│   ├── nginx.template.conf
│   └── provisioning_notes.md
├── functional_tests │
── __init__.py │
├── [...] ├── lists
│   ├── __init__.py
│   ├── models.py
│   ├── static
│   │   ├── base.css
│   │   ├── [...]
│   ├── templates
│   │   ├── base.html
│   │   ├── [...]
├── manage.py
├── requirements.txt
└── superlists
├── [...]
