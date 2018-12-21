from django.contrib import admin
from myblog.models import Category, Post, User, Tag, Comment


class PostAdmin(admin.ModelAdmin):
	list_display = ['title','create_time','modify_time','category','user']
	

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
# Register your models here.
