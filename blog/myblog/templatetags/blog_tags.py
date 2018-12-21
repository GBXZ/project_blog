from django import template
from myblog.models import Post, Category, Tag


register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-create_time')[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('create_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.all()[:5]


@register.simple_tag
def get_tag():
    return Tag.objects.all()
