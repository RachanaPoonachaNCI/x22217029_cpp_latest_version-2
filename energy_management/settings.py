"""
Django settings for energy_management project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-$s(@2rqs%8k+y-q-w%cv2sz%d+r=edxj&x!&7g@q@0!yd29_^z"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['x22217029-rachana.eba-pe9sxm8x.sa-east-1.elasticbeanstalk.com','54.94.28.77','3.253.239.218','127.0.0.1:8000','172.31.26.141','172.31.35.132','51.20.222.174','x22217029cpp-env2.eba-hemqevvf.sa-east-1.elasticbeanstalk.com','16587ee00eb34e81aa0fe948fe97ab2b.vfs.cloud9.eu-north-1.amazonaws.com','51.20.249.35','16.16.246.142','x22217029cpp-env.eba-gwxdfpri.eu-north-1.elasticbeanstalk.com','x22217029cpplatest-env.eba-gwxdfpri.eu-north-1.elasticbeanstalk.com','x22217029cpp-env-4.eba-7mqmtqfh.eu-north-1.elasticbeanstalk.com','127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://c7403b93921e47b194ab5e41acac01b6.vfs.cloud9.eu-west-1.amazonaws.com','https://3.249.208.143','https://3.252.138.102','http://51.20.222.174','https://3.253.155.8','https://3.250.149.11','https://3.253.239.218','https://x22217029-rachana.eba-pe9sxm8x.sa-east-1.elasticbeanstalk.com','http://127.0.0.1:8000/','http://172.31.26.141','http://172.31.35.132','http://51.20.249.35','http://16.16.246.142','http://x22217029cpplatest-env.eba-gwxdfpri.eu-north-1.elasticbeanstalk.com','http://x22217029cpp-env-4.eba-7mqmtqfh.eu-north-1.elasticbeanstalk.com/','http://127.0.0.1']

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "authentication.apps.AuthenticationConfig",
    "energy_analysis.apps.EnergyAnalysisConfig",
    "storages",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "energy_management.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "energy_management.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

#Postgres connection details being retrieved through secret file
from aws_cloud_services.db_secret import get_secret
database_secret =  get_secret()
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': database_secret['dbname'],
            'USER': database_secret['username'],
            'PASSWORD': database_secret['your_password_key'],
            'HOST' : 'x22217029-postgres-db-cpp.ctawtprtjx6u.eu-north-1.rds.amazonaws.com',
            'PORT': '5432',
        }
    }

#s3 bucket credentials retrieved by importing config file which has environment variables defined
from aws_cloud_services.s3_credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME
AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
AWS_S3_REGION_NAME = AWS_S3_REGION_NAME
AWS_STORAGE_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = 'eu-north-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' 



AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

#STATIC_URL = "static/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SESSION_COOKIE_HTTPONLY = False
