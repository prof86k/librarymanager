from django.contrib import admin

# Register your models here.
from . import models as mdl

admin.site.register(mdl.Administrator)
admin.site.register(mdl.Student)
