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

# CKeditor

Install Command Line Tools:
    https://developer.apple.com/download/more/