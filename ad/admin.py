from django.contrib import admin
from .models import AD, Image


class ImageInLine(admin.StackedInline):
    model = Image


class ADAdmin(admin.ModelAdmin):
    inlines = (ImageInLine,)


admin.site.register(AD, ADAdmin)
