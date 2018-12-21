from django.contrib.syndication.views import Feed
from myblog.models import Post
from django.urls import reverse


class PostFeed(Feed):
    title = '博客新文章'
    link = '/feeds/'
    description = '文章有新的更新'

    def items(self):
        return Post.objects.all().order_by('-create_time')[:3]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body[:30]

    def item_link(self, item):
        return 'http://127.0.0.1:8000/myblog/detail/'+str(item.id)+'/'


