from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'netvizor-secret-key'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = ['django.contrib.staticfiles','scanner']
MIDDLEWARE = [
 'django.middleware.security.SecurityMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
]
ROOT_URLCONF = 'netvizor.urls'
TEMPLATES = [{
 'BACKEND':'django.template.backends.django.DjangoTemplates',
 'DIRS':[BASE_DIR/'templates'],
 'APP_DIRS':True,
 'OPTIONS':{'context_processors':[
  'django.template.context_processors.debug',
  'django.template.context_processors.request',
 ]},
}]
WSGI_APPLICATION = 'netvizor.wsgi.application'
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR/'static']
