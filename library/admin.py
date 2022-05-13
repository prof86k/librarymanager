from django.contrib import admin

# Register your models here.
from . import models as mdl

admin.site.register(mdl.Shelve)
admin.site.register(mdl.Book)