from django.db import models
from django.contrib.auth.models import User
import markdown
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name = u"分类名字")
    class Meta:
        verbose_name = u"分类"
        verbose_name_plural = verbose_name
        db_table = 'category'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"标签")

    class Meta:
        verbose_name = u"标签"
        verbose_name_plural = verbose_name
        db_table = 'tag'

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200,verbose_name=u"标题")
    body = models.TextField(verbose_name=u"文章正文")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')
    modify_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    excerpt = models.CharField(max_length=200, blank=True, verbose_name=u'文章摘要')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=u'文章分类')
    tags = models.ManyToManyField(Tag, verbose_name=u'标签')
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name=u'作者')
    views = models.PositiveIntegerField(default=0, verbose_name=u'阅读量')

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name
        db_table = 'post'

    def __str__(self):
        return self.title
#
# # 重写保存方法
# 	def save(self, *args, **kwargs):
# 		# 如果没有摘要， 从body取出一部分
# 		if not self.excerpt:
# 			# 实例化md，用于渲染body文本
# 			md = markdown.Markdown(extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
# 		# 将md文本渲染成html
# 		# strip_tags 去掉html文本的全部html标签
# 		# 摘取body前54个给excerpt
# 		self.excerpt = strip_tags(md.convert(self.body))[:54]


class Comment(models.Model):
    wb_id = models.CharField(max_length=100, verbose_name=u'评论者微博id')
    name = models.CharField(max_length=200, verbose_name=u'评论者微博姓名')
    profile_image_url = models.CharField(max_length=500, verbose_name=u'评论者微博头像')
    comment = models.TextField(verbose_name='评论')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=u'文章')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = 'comment'
        verbose_name = u'评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Userinfo(models.Model):
    wb_id = models.CharField(max_length=50, verbose_name=u'新浪用户id', null=True)
    name = models.CharField(max_length=200, verbose_name=u'新浪用户名称', null=True)
    profile_image_url = models.CharField(max_length=500, verbose_name=u'用户头像', null=True)

    class Meta:
        db_table = 'user_info'
        verbose_name = u'用户信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

