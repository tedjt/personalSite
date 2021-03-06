from .models import Blog, Post
from datetime import datetime
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed
from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template
from simplesocial.api import wide_buttons, narrow_buttons


POSTS_PER_PAGE = 8

def review(request, review_key):
    post = get_object_or_404(Post, review_key=review_key)
    return show_post(request, post, review=True)

def show_post(request, post, review=False):
    recent_posts = Post.objects.filter(blog=post.blog, published=True)
    recent_posts = recent_posts.order_by('-published_on')[:6]
    return direct_to_template(request, 'blog/post_detail.html',
        {'post': post, 'blog': post.blog, 'recent_posts': recent_posts,
         'review': review})

def browse(request, blog):
    if request.GET.get('page') == '1':
        return HttpResponseRedirect(request.path)
    query = Post.objects.filter(blog=blog, published=True)
    query = query.order_by('-published_on')
    # TODO: add select_related('author')
    return object_list(request, query, paginate_by=POSTS_PER_PAGE,
        extra_context={'blog': blog, 'recent_posts': query[:6],
                       'browse_posts': True})

def feedburner(feed):
    """Converts a feed into a FeedBurner-aware feed."""
    def _feed(request, blog):
        if not blog.feed_redirect_url or \
                request.META['HTTP_USER_AGENT'].startswith('FeedBurner') or \
                request.GET.get('override-redirect') == '1':
            return feed(request, blog=blog)
        return HttpResponseRedirect(blog.feed_redirect_url)
    return _feed

class LatestEntriesFeed(Feed):
    feed_type = Atom1Feed

    def get_object(self, request, blog):
        return blog

    def title(self, blog):
        return '%s - %s' % (blog.title, settings.SITE_NAME)

    def link(self, blog):
        return blog.get_absolute_url()

    def subtitle(self, blog):
        return blog.description

    def item_title(self, post):
        return post.title

    def item_description(self, post):
        url = 'http%s://%s%s' % ('s' if self._request.is_secure() else '',
                                 self._request.get_host(),
                                 post.get_absolute_url())
        header = wide_buttons(self._request, post.title, post.get_absolute_url())
        footer = narrow_buttons(self._request, post.title, post.get_absolute_url())
        footer += '<p><a href="%s#disqus_thread">Leave a comment</a></p>' % url
        return header + post.rendered_content + footer

    def item_author_name(self, post):
        return post.author.get_full_name()

    def item_pubdate(self, post):
        return post.published_on

    def items(self, blog):
        query = Post.objects.filter(blog=blog, published=True).order_by(
            '-published_on')
        # TODO: add select_related('author') once it's supported
        return query[:100]

@feedburner
def latest_entries_feed(request, *args, **kwargs):
    feed = LatestEntriesFeed()
    feed._request = request
    return feed(request, *args, **kwargs)
