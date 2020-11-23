# TEMPLATES

    put them in settings.py file
    TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...

## URL

    in main project urls.py add:
        from django.urls import path, include

        urlpatterns = [
            path('', include('pages.urls')),
        ...

## STATIC FILES & PATHS

    settings.py   --> in STATIC section add
        STATIC_ROOT = os.path.join(BASE_DIR, 'static')
        STATIC_URL = '/static/'
        STATICFILES_DIRS = [
            os.path.join(BASE_DIR, 'btre/static')   <--- this file contains  all js, css, img and lightbox>
        ]

    RUN:
        $ python manage.py collectstatic

    Add the css and js files into the base.html and add this line at the top pf the base.html file

    {% load static %}
    <link rel="stylesheet" href="{% static 'css/all.css' %}">

    TODO: Copy css files from btr app

## MEDIA/Model images

do this so the media files to show up in the frontend

* note. If wanted add the models to the admin section
in admin.py of each project add

admin.site.register(Listing, ListingAdmin)


Open settings.py and at the bottom add

-- MEDIA folder settings

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

Open [main project]/urls.py add to the urlpatterns:

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('listings/', include('listings.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

## MODIFY Admin site

    check admin.py in each app: i.e.:
    from django.contrib import admin
    from .models import Listing

    class ListingAdmin(admin.ModelAdmin):
        list_display = ('id', 'title', 'is_published', 'price', 'list_date', 'realtor')
        list_display_links = ('id', 'title')
        list_filter = ('realtor',)
        list_editable = ('is_published',)
        search_fields = ('title', 'description', 'address', 'city', 'state', 'zipcode', 'price')
        list_perpage = 25

    admin.site.register(Listing, ListingAdmin

## Edit VSCODE settings

Install pip install pylint-django
{
    "editor.fontSize": 16,
    "editor.wordWrap": "on",
    "editor.tabSize": 2,
    "explorer.confirmDragAndDrop": false,
    "python.linting.pylintArgs": [
        "--load-plugins=pylint_django"
    ],   <=== Remove error marks in Model.objects
    "terminal.integrated.fontSize": 14
}

## CKeditor

Install Command Line Tools:
    https://developer.apple.com/download/more/

## HEROKU setup

$ heroku login
    It will ask for your password and username
$ heroku keys:add
    It will found the key and say yes  <--- this key was created before.
$ heroku create
    It will create an app in heroku

INSTALL apps:
    Web Server that Heroku uses for Django projects

    Head over to the terminal
        $ pip install gunicorn
        $ pip install django-heroku   ----> this installs whitenoise (handles static files)
        $ pip install python-decouple

Create/modify files that heroku needs

in settings.py

    add:
        import django_heroku
        from decouple import config
        import dj_database_url   ---> We are gonna setup a postgres db up at heroku and there's gonna be settings involved in that, things like username, password, url and those things change every 24 hours automatically so this app takes care of all those changes behind the scenes for you

        Put a setting down below for django_heroku
        django_heroku.settings(locals())

        Take care of the SECRET_KEY, located in settings.py
        Copy the SECRET_KEY value and log back to heroku on your apps, look for your app and open it.
        Go to settings tag, click on 'Reveal config vars' button, add your key as
            SECRET_KEY = 'VALUE copied'   ---> that's it

            Back in settings.py Change SECRET_KEY as follows:
                - move the secret_key value to an environmental variable file, and this file will be hidden from GIT.
                - in main directory from terminal:
                    $ touch .env
                    copy the SECRET_KEY and value and paste it into .env file 
                - create SECRET_KEY = config('SECRET_KEY')
                - add .env file to .gitignore

    Whitenoise:
        - Add STATICFILES_DIRS (done)
        - in MIDDLEWARE Section below SecurityMiddleware:
            'whitenoise.middleware.WhiteNoiseMiddleware',
        - Add STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'   --> it zips all static files

Create Procfile and Requirements.txt
    Procfile tells heroku what kind of app this is.
    $ touch Procfile  ---> inside paste:
        web: gunicorn fercodes.wsgi

    Requirements.txt
    Heroku needs a list of all the requirements (apps installed)
    $ pip freeze shows all the requirements.
    execute this command and copy the outcome: 
        $ pip freeze > requirements.txt

Push to heroku

$ git push heroku master

Migrate in heroku. any command run locally can be run in heroku by this command heroku run
$ heroku run python manage.py makemigrations
$ heroku run python manage.py migrate

.
On heroku web in your app, click on heroku postgresql db button, click on overview --> Database credentials and copy the Databse URI credential and paste in **.

In settings.py file modify DATABASES section:
    ENGINE : django.db.backends.postgresql_psycopg2,
    REMOVE OTHER properties in default

Outside DATABASES section:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
        }
    }
    # This allows to connect directly to heroku db and local db
    ** DATABASES['default'] = dj_database_url.config(default='postgres://hmqsenxdruirjn:6f6f796ae75aff256539332cd3299e55c4f7b8b53a847eaf121c027e7f1b838b@ec2-23-23-242-234.compute-1.amazonaws.com:5432/d6ihbgrfj6jt2')

    db_from_env = dj_database_url.config(conn_max_age=600)
    DATABASES['default'].update(db_from_env)


CUSTOM DOMAIN and HEROKU

In heroku go to the app, settings, down at the bottom click on add domain button and type in the domain name.

google: buy a domain on Namecheap and pointing to heroku:
    lewagon.com/buying-a-domain-on-namecheap-and-pointing-to-heroku....

    On namecheap -> domain-list -> CNAME Record type heroku app name and put . (dot) at the end of the url 
