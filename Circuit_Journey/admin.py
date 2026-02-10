from django.contrib import admin
from .models import *

# Register your models here.
from django.contrib import admin
from .models import Blog, Categories



admin.site.register(Blog)
admin.site.register(Categories)
admin.site.register(Comments)
