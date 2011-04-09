from .models import Page
from django.views.generic.simple import direct_to_template
from urlrouter.base import URLHandler

class PageRoutes(URLHandler):
    model = Page

    def show(self, request, page):
        if(page.url=="/home/" or page.url=="/home"):
            return direct_to_template(request, 'minicms/home.html',
                {'page': page})
        else:
            return direct_to_template(request, 'minicms/page_detail.html',
                {'page': page})