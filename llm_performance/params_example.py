from __future__ import unicode_literals

#--- Django
ENV = 'development'
# ENV = 'production'
# ENV = 'docker'
# DEBUG = True
# RAISE_EXCEPTIONS = True
# SECRET_KEY = 'must be declared here !!!'
# SITE_BASE_URL = ''

#--- Log files permission fix
import os
os.umask(0o002)

#--- Sentry
# SENTRY_ENABLED = False
# SENTRY_DSN = ''

#--- SQlite3
# DATABASES_ENGINE = 'django.db.backends.sqlite3'
# DATABASES_NAME = 'db.sqlite'

#--- Oracle
# DATABASES_ENGINE = 'django.db.backends.oracle'
# DATABASES_NAME = 'xe'
# DATABASES_USER = 'system'
# DATABASES_PASSWORD = '<password>'
# DATABASES_HOST = 'localhost'
# DATABASES_PORT = '49161'
# DATABASES_OPTIONS = {}
# DATABASES_TEST = dict(NAME='unittest.db')
# DATABASES_CONN_MAX_AGE = 0

#--- Postgres
# DATABASES_ENGINE = 'django.db.backends.postgresql'
# DATABASES_NAME = 'llm_performance_db_01'
# DATABASES_USER = 'llm_performance_db_user'
# DATABASES_PASSWORD = '<password>'
# DATABASES_HOST = 'localhost'
# DATABASES_PORT = ''

#--- Database Backups
# DBBACKUP_STORAGE_OPTIONS = {'location': '/tmp'}

#--- EMAIL
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'your_account@gmail.com'
# EMAIL_HOST_PASSWORD = 'password is secret'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_ADMIN = f'admin@{SITE_BASE_URL}'

#--- Google reCaptcha Keys
# GOOGLE_RECAPTCHA_SECRET_KEY = 'dummy_secret_key'
# GOOGLE_RECAPTCHA_SITE_KEY = 'dummy_site_key'

#--- Account & Auth
# ACTIVATION_CODE_EXPIRING_MINUTE = 15

#--- Admin Panel Restrictions
# RESTRICT_ADMIN = True
# ALLOWED_ADMIN_IPS = ['127.0.0.1', '::1']
# ALLOWED_ADMIN_IP_RANGES = ['127.0.0.0/24', '::/1']
# RESTRICTED_APP_NAMES = ['admin']
# TRUST_PRIVATE_IP = True
