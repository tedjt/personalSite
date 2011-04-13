from .models import Block, Page
from django.contrib import admin
from django.contrib.admin.widgets import AdminTextareaWidget
from django.db import models

class CommonMedia:
    js = (
    'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
    '/media/admin/js/dojoEditor.js',
  )
    css = {
    'all': ('/media/admin/css/editor.css',),
    }
# The default TextField doesn't have enough rows
class UsableTextarea(AdminTextareaWidget):
    def __init__(self, attrs=None):
        default_attrs = {'rows': '32'}
        if attrs:
            default_attrs.update(attrs)
        super(UsableTextarea, self).__init__(default_attrs)

class BaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': UsableTextarea},
    }

class PageAdmin(BaseAdmin):
    fields = ('url', 'title', 'content', 'show_share_buttons', 'raw_html')
    list_display = ('url', 'title', 'show_share_buttons', 'raw_html')
    search_fields = ('url',)
    ordering = ('url',)

class BlockAdmin(BaseAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Page, PageAdmin, Media = CommonMedia)
admin.site.register(Block, BlockAdmin)
