# LLM performance statistics

CPU & GPU performance measures of LLM engine



## Get Started

Clone project files locally.

If you are running on production server please use a separate user `user` and run all applications on behalf of the `user`, not `root`:

        sudo adduser user
        sudo usermod -aG sudo user
        sudo su user
        cd ~
        git clone https://github.com/datahaven-net/llm-performance.git
        cd llm-performance


Install required packages:

        sudo apt-get install make python3-pip python3-dev python3-venv libpq-dev postgresql postgresql-contrib memcached uwsgi-plugins-all

 
Create DB and user:

        sudo su - postgres

        postgres@test:~$ psql
        psql (9.3.22)
        Type "help" for help.

        postgres=# CREATE DATABASE llm_performance_db_01;
        CREATE DATABASE

        postgres=# CREATE USER llm_performance_db_user WITH PASSWORD '<password>';
        CREATE ROLE

        postgres=# ALTER ROLE llm_performance_db_user SET client_encoding TO 'utf8';
        ALTER ROLE

        postgres=# ALTER ROLE llm_performance_db_user SET default_transaction_isolation TO 'read committed';
        ALTER ROLE

        postgres=# ALTER ROLE llm_performance_db_user SET timezone TO 'UTC';
        ALTER ROLE

        postgres=# GRANT ALL PRIVILEGES ON DATABASE llm_performance_db_01 TO llm_performance_db_user;
        GRANT

        \q
        exit


To be able to run same code on production machine as well as locally on your laptop you can use isolated development settings, configure this by setting `src/main/params.py` file:

        cp llm_performance/params_example.py llm_performance/params.py
        nano llm_performance/params.py


Set those settings in your `params.py` file if you starting a new production machine:

        ENV = 'production'
        DATABASES_ENGINE = 'django.db.backends.postgresql'
        DATABASES_NAME = 'llm_performance_db_01'
        DATABASES_USER = 'llm_performance_db_user'
        DATABASES_PASSWORD = '<password>'
        DATABASES_HOST = 'localhost'
        DATABASES_PORT = ''


To run locally you can use SQLite3:

        ENV = 'development'
        DATABASES_ENGINE = 'django.db.backends.sqlite3'
        DATABASES_NAME = 'db.sqlite'


Create virtual environement if you do not have yet:

        make venv


Run Django migrate command:

        make migrate


Run Django collectstatic command:

        make collectstatic


Create Django super user:

        make createsuperuser


Launch Django server to test the configuration:

        make runserver


Now you can navigate your browser to `http://127.0.0.1:8000/` and visit the web site which is running locally.



## Running on production

For production configuration you can take a look at some examples in `etc/` folder.

You might want to use your own tweaks for nginx and uwsgi, so those files are just a starting point for you.
Configuration here was tested on Ubuntu 18.04.1 LTS server.

First we create a separate folder to store all interesting logs in one place. And we need to configure our log rotation:

        mkdir /home/user/llm-performance/log/
        sudo chown www-data:user -R /home/user/llm-performance/log/
        sudo cp etc/logrotate.d/llm-performance.example /etc/logrotate.d/llm-performance
        sudo nano /etc/logrotate.d/llm-performance  # modify the file with your actual configuration


Add `www-data` user to `user` group so uwsgi process will be able to access log files created by Django:

        sudo usermod -a -G user www-data


Make sure you set the correct domain name on your server:

        sudo hostname -b yourdomain.com


Install nginx if you do not have it yet installed:

        sudo apt-get install nginx


Activate nginx site configuration by creating a sym-link:

        cp etc/nginx/llm-performance.example etc/nginx/llm-performance
        sudo ln -s /home/user/llm-performance/etc/nginx/llm-performance /etc/nginx/sites-enabled/llm-performance
        sudo unlink /etc/nginx/sites-enabled/default
        sudo nano /etc/nginx/sites-enabled/llm-performance  # modify the file with your actual configuration


To secure your site you need to configure SSL certificate. Check `etc/nginx/llm-performance` file to configure crtificate and key files location. Here is an example SSL config you can use to build your setup:

        ssl_certificate     /home/user/ssl/llm-performance.crt;
        ssl_certificate_key /home/user/ssl/llm-performance.key;
        ssl_ciphers         EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH;
        ssl_protocols       TLSv1.1 TLSv1.2;


Now it is time to configure uwsgi in emperor mode to follow best practices.
We will need one vassal to be running and serving web site traffic.

The main uwsgi emperor process will be starting as systemd service:

        cp etc/uwsgi/emperor.ini.example etc/uwsgi/emperor.ini
        nano etc/uwsgi/emperor.ini  # modify the file with your actual configuration

        cp etc/uwsgi/vassals/llm-performance.ini.example etc/uwsgi/vassals/llm-performance.ini
        nano etc/uwsgi/vassals/llm-performance.ini  # modify the file with your actual configuration

        cp etc/systemd/system/uwsgi-emperor.service.example etc/systemd/system/uwsgi-emperor.service
        sudo ln -s /home/user/llm-performance/etc/systemd/system/uwsgi-emperor.service /etc/systemd/system/uwsgi-emperor.service
        sudo nano /etc/systemd/system/uwsgi-emperor.service  # modify the file with your actual configuration


Now start uwsgi emperor service:

        sudo systemctl start uwsgi-emperor.service


You can always check current situation with:

        systemctl status uwsgi-emperor.service


Finally restart nginx server to make everything work end-to-end:

        sudo service nginx restart


At any moment you can gracefully respawn web site process manually by "touching" llm-performance.ini file:

        touch /home/user/llm-performance/etc/uwsgi/vassals/llm-performance.ini


Your live server should be up and running now, navigate your browser to http://www.yourdomain.com

But you will need a to do a bit more configurations on Production server later on, read more about that bellow after you finish preparing other parts of the system.



## Django settings

In the file `llm-performance/params.py` you will have to set few important variables.

Those settings are specific for your host machine and can not be stored in the source code. Also this file is a place to store keys, passwords, etc.

Other settings in `params.py` file also described in that document, but here is a list of most important settings:

* `ENV = 'production'` : this will identify your production machine
* `DEBUG = False` : must be always `False` on your production machine
* `SITE_BASE_URL = 'https://yourdomain.com'` : domain name of your host
* `SECRET_KEY = 'xxxx'` : django key to be used to encrypt user sessions, must be 50 bytes long



## Configure Email settings

If it is required you cat enable user account activations via email. To do that edit file `llm-performance/params.py` and add such line:

        ENABLE_USER_ACTIVATION = True


Also you have to configure outgoing email channel to deliver messages. Different backends can be used in Django, simplest way to start with Google Accounts SMTP service:

        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_HOST_USER = 'my_gmail_login@gmail.com'
        EMAIL_HOST_PASSWORD = '<password>'
        EMAIL_PORT = 587
        EMAIL_USE_TLS = True
        EMAIL_USE_SSL = False



## Configure Memcache

TODO: memcached...



## Configure Googla Captcha

If you want users to see Google Captcha in login screen, you need to go to https://www.google.com/recaptcha/ and setup captcha for your website.
In order to setup, you can check Google documentation here: https://developers.google.com/recaptcha

Once you have site key and secret key for your website, you should edit `llm-performance/params.py` file and set `GOOGLE_RECAPTCHA_SITE_KEY` and `GOOGLE_RECAPTCHA_SECRET_KEY` constants.

If you don't want to enable Google captcha for your local environment or for your website, you can set `GOOGLE_RECAPTCHA_SITE_KEY = None`.



## Database Backups

In params.py file, storage location should be defined.

        DBBACKUP_STORAGE_OPTIONS = {'location': '/tmp/'}

To backup your database, use below Django command.

        ./venv/bin/python manage.py dbbackup

 To restore latest backup for database, use below Django command.

        ./venv/bin/python manage.py dbrestore

There are more options to use for database backups like compressing, encrypyting etc.
Go to [django-dbbackup](https://django-dbbackup.readthedocs.io/en/stable/commands.html) documentation for more info.



## Requirements Handling

The project has automated handling of production requirements, the idea behind it is that
you should always use the latest versions of every requirement, a Makefile target is in place
to update the `requirements.txt` file (`make requirements.txt` will do).

In case you need a specific version of a library, the protocol should be:

* Place the needed fixed version using pip notation in any of the requirements/* files
* Put a comment over the fixed requirement explaining the reason for fixing it (usually with a link to an issue/bug)
* Run `make requirements.txt`, the resulting requirements file will include the fixed version of the package

For some more advanced uses, a manual edit of the requirements.txt can be done but make sure to document it somewhere because `make requirements.txt` *will* overwrite this file.



# Testing against latest versions

By default, `tox` and `make test` will only test against production requirements, in order to test against latest versions of the dependencies, there are two tox environments, `latest27` and `latest35`.

They can be run via `tox -e latest27,latest35` or also with `make test_latest`



## Contributing

Please go to [Main GitHub repository](https://github.com/datahaven-net/llm-performance), click "Fork", and clone your fork repository via git+ssh link:

        git clone git@github.com:< your GitHub username here >/llm-performance.git


Then you need to add the main repo as "upstream" source via HTTPS link (in read-only mode):

        cd llm-performance
        git remote add upstream https://github.com/datahaven-net/llm-performance.git
        git remote -v
        origin  git@github.com:< your GitHub username here >/llm-performance.git (fetch)
        origin  git@github.com:< your GitHub username here >/llm-performance.git (push)
        upstream    https://github.com/datahaven-net/llm-performance.git (fetch)
        upstream    https://github.com/datahaven-net/llm-performance.git (push)


Your current forked repository remains as "origin", and you should always commiting and pushing to your own code base:

        # after you made some modifications, for example in README.md
        git add README.md
        git commit -m "updated documentation"
        git push origin master


Then you start a [new Pull Request](https://github.com/datahaven-net/llm-performance/compare) towards main repository, you can click "compare across forks" link to select your own repository source in "head fork" drop down list. Then you will see the changes you are going to introduce and will be able to start the Pull Request.

Please cooperate with the community to make your changes Approved and Merged into the main repository. As soon as your Pull Request was merged, you can refresh your local files and "origin" repository:

        git pull upstream master
        git push origin master



### Gather info about your CPU

Linux:

        lscpu | grep "Model name:"


MacOS:

        sysctl -a | grep machdep.cpu.brand_string:


Windows (via cmd.exe):

        wmic cpu get name



### Gather info about your GPU

Linux:

        lspci | grep ' VGA '


MacOS:

        system_profiler SPDisplaysDataTypes


Windows (via cmd.exe):

        wmic path win32_VideoController get name
