from django.contrib import admin
from gif.models import Gif, Tag, Category

admin.site.register([Gif, Tag, Category])
