import time


from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.views.generic.base import View
from myblog import models
from django.core.paginator import Paginator # 分页
from django.conf import settings
import markdown  #代码高亮
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #  purepagination分页
from myblog.wb_oauth import OAuthWB  # 微博认证
from myblog.send_email import send_email


WEIBO_APP_ID = '205667593'  # App key
WEIBO_APP_KEY = 'a6daff4e316097b8c5cab6f3cd95ef06'   # App secret
WEIBO_REDIRECT_URL = 'http://127.0.0.1:8000/myblog/weibo/connect/callback.php' #微博回调地址


# 主页
class Index(View):
	def get(self, request):
		post_list = models.Post.objects.all().order_by('-create_time')
		# 查询出归档日期的文章
		year = request.GET.get('year', '')
		month = request.GET.get('month', '')
		category = request.GET.get('category', '')
		if year and month:
			post_list = models.Post.objects.filter(create_time__year=int(year), create_time__month=int(month)) \
				.order_by('-create_time')
		# 查询出分类的文章
		if category:
			post_list = models.Post.objects.filter(category__name=category)

		# 使用pure_pagination 进行分页代码
		try:
			page = request.GET.get('page', 1)
		except:
			page = 1
		p = Paginator(post_list, 3, request=request)   # 中间的1 是每页显示的数量
		posts = p.page(page)
		# 查询出总共页数
		p = Paginator(post_list, 3)
		page_total = p.num_pages

		# 使用 django pagintor 进行分页代码
		# page_num = int(request.GET.get('page', 1))
		# p = Paginator(post_list, 1)
		# if int(page_num) == 1:
		# 	x = 1
		# else:
		# 	x = int(page_num)
		# 	x = x - 1
		# if page_num == p.num_pages:
		# 	y = int(p.num_pages)
		# else:
		# 	y = int(page_num)
		# 	y = y+1
		# page_total = p.num_pages
		# post_list = p.page(1)
		name = request.session.get('name')
		profile_image_url = request.session.get('profile_image_url')
		return render(request, 'myblog/index.html', locals())

	def post(self, request):
		search_feild = request.POST.get('search', '')
		post_list = models.Post.objects.filter(title__icontains=search_feild)
		try:
			page = request.GET.get('page', 1)
		except:
			page = 1
		p = Paginator(post_list, 3, request=request)  # 中间的1 是每页显示的数量
		posts = p.page(page)
		# 查询出总共页数
		p = Paginator(post_list, 3)
		page_total = p.num_pages
		return render(request, 'myblog/index.html', locals())


# 文章详细信息
class Detail(View):
	def get(self, request, pk):
		# get_object_or_404 有两个参数，第一个是查询源，第二个条件，如果查询为空返回404页面
		post = get_object_or_404(models.Post, id=pk)
		post_id = pk
		# markdown标记语言
		# post.body = markdown.markdown(post.body, extensions=[
		# 	'markdown.extensions.extra',
		# 	'markdown.extensions.codehilite',
		# 	'markdown.extensions.toc',
		# ])
		comments = models.Comment.objects.filter(post_id=int(pk))
		# 标记语言以及生成目录列表
		md = markdown.Markdown(extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
			'markdown.extensions.toc',
		])
		post.body = md.convert(post.body)
		toc = md.toc
		# post.increase_views用来自增长阅读量
		post.increase_views()
		name = request.session.get('name')

		return render(request, 'myblog/single.html', locals())

	def post(self, request, pk):
		search_field = request.POST.get('search', '')
		post_list = models.Post.objects.filter(title__icontains=search_field)
		if search_field:
			try:
				page = request.GET.get('page', 1)
			except:
				page = 1
			p = Paginator(post_list, 3, request=request)  # 中间的1 是每页显示的数量
			posts = p.page(page)
			# 查询出总共页数
			p = Paginator(post_list, 3)
			page_total = p.num_pages
			return render(request, 'myblog/index.html', locals())
		# 生成评论
		else:
			name = request.session.get('name')
			wb_id = request.session.get('wb_id')
			profile_image_url = request.session.get('profile_image_url')
			comment = request.POST.get('comment', '')
			new_comment = models.Comment()
			new_comment.post_id = int(pk)
			new_comment.name = name
			new_comment.wb_id = wb_id
			new_comment.profile_image_url = profile_image_url
			new_comment.comment = comment
			new_comment.save()
			return redirect('/myblog/detail/{0}'.format(pk))


# 归档显示
# class Archives(View):
# 	def get(self, request):
# 		year = request.GET.get('year', '')
# 		month = request.GET.get('month', '')
# 		# 条件查询出某年某月的文章
# 		post_list = models.Post.objects.filter(create_time__year=int(year), create_time__month=int(month ))\
# 			.order_by('-create_time')
# 		return render(request, 'myblog/index.html', locals())

# Create your views here.
# class Search_post(View):
# 	def post(self):

#微博登陆, 引导用户到这个模块
def weibo_login(request):
	return HttpResponseRedirect('https://api.weibo.com/oauth2/authorize?client_id=' + WEIBO_APP_ID + '&redirect_uri=' + WEIBO_REDIRECT_URL)


# 获取用户微博信息
def weibo_get_code(request):
	code = request.GET.get('code', None)
	sina = OAuthWB(client_id=WEIBO_APP_ID, client_key=WEIBO_APP_KEY, redirect_url=WEIBO_REDIRECT_URL)
	access_token_data = sina.get_access_token(code)
	time.sleep(0.1)
	user_info = sina.get_user_info(access_token_data)
	# 获取用户名
	name = user_info['name']
	# 获取用户头像链接
	profile_image_url = user_info['profile_image_url']
	# 获取用户微博id
	wb_id = user_info['id']
	# user_info_msg = models.Userinfo()
	# user_info_msg.wb_id = wb_id
	# user_info_msg.name = name
	# user_info_msg.profile_image_url = profile_image_url
	# user_info_msg.save()
	request.session['wb_id'] = wb_id
	request.session['name'] = name
	request.session['profile_image_url'] = profile_image_url
	return redirect('http://127.0.0.1:8000/myblog/index/')


# 关于自己
class Formyself(View):
	def get(self,request):
		return render(request, 'myblog/about.html')

	def post(self,request):
		search_field = request.POST.get('search', '')
		post_list = models.Post.objects.filter(title__icontains=search_field)
		if search_field:
			try:
				page = request.GET.get('page', 1)
			except:
				page = 1
			p = Paginator(post_list, 3, request=request)  # 中间的1 是每页显示的数量
			posts = p.page(page)
			# 查询出总共页数
			p = Paginator(post_list, 3)
			page_total = p.num_pages
			return render(request, 'myblog/index.html', locals())


# 联系我
class Contact(View):
	def get(self, request):
		return render(request, 'myblog/contact.html')

	def post(self, request):
		search_field = request.POST.get('search', '')
		post_list = models.Post.objects.filter(title__icontains=search_field)
		if search_field:
			try:
				page = request.GET.get('page', 1)
			except:
				page = 1
			p = Paginator(post_list, 3, request=request)  # 中间的1 是每页显示的数量
			posts = p.page(page)
			# 查询出总共页数
			p = Paginator(post_list, 3)
			page_total = p.num_pages
			return render(request, 'myblog/index.html', locals())
		else:
			name = request.POST.get('name')
			email = request.POST.get('email')
			subject = request.POST.get('subject')
			message = request.POST.get('message')
			message = '联系人姓名： %s ，联系人邮箱：%s，联系人发送的信息：%s' % (name, email, message)
			send_email(subject=subject, message=message)
			return HttpResponse('ok')


class Full_width(View):
	def get(self, request):
		post_list = models.Post.objects.all().order_by('create_time')
		try:
			page = request.GET.get('page', 1)
		except:
			page = 1
		p = Paginator(post_list, 5, request=request)  # 中间的1 是每页显示的数量
		posts = p.page(page)
		# 查询出总共页数
		p = Paginator(post_list, 5)
		page_total = p.num_pages
		return render(request, 'myblog/full-width.html', locals())

	def post(self, request):
		search_field = request.POST.get('search', '')
		post_list = models.Post.objects.filter(title__icontains=search_field)
		if search_field:
			try:
				page = request.GET.get('page', 1)
			except:
				page = 1
			p = Paginator(post_list, 3, request=request)  # 中间的1 是每页显示的数量
			posts = p.page(page)
			# 查询出总共页数
			p = Paginator(post_list, 3)
			page_total = p.num_pages
			return render(request, 'myblog/index.html', locals())