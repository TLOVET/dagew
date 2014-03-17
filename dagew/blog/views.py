#coding:utf8

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,InvalidPage
from django.contrib.auth.models import User
from django.contrib.auth  import login,logout,authenticate
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import time
import  json

from blog.models import Dish,Restaurant,Notice,UserProfile,Mall,Order

totil=0
#处理滚动新闻的显示内容
notices=Notice.objects.all()
b=[]
for i in notices:
	b.append({'content':i.notice_content,'url':i.notice_url})
tongzhi=json.dumps(b)

#当点击页面中注册时，实现局部刷新
def regist(req):
	return HttpResponse('zhuce')

#处理注册的界面的数据，并保存到数据库
def regist_1(req):
	if req.method=='POST':
		username=req.POST['username']
		password=req.POST['password']
		email=req.POST['email']
		area=req.POST['area']
		address=req.POST['address']
		tel=req.POST['tel']
		u=User.objects.create_user(username=username,password=password,email=email)
		UserProfile.objects.create(area=area,address=address,tel=tel,user=u,credit=10)
		return HttpResponseRedirect('/login/')
	return render_to_response('index.html')

#auth自带用户登录并认证
def user_login(req):
	req.session['totil']=0
	req.session['caidan']=[]
	userprofiles=UserProfile.objects.all().order_by('-credit')[:5]
	restaurants=Restaurant.objects.all()
	dishs=Dish.objects.all()[:8]
	notice=tongzhi
	if req.method=='POST':
		username=req.POST['username']
		password=req.POST['password']
		user=authenticate(username=username, password=password)
		if user:
			login(req,user)
			return HttpResponseRedirect('/index/')
	return render_to_response('index.html',locals())

#处理主页
def index(req):
	userprofiles=UserProfile.objects.all().order_by('-credit')[:5]
	notice=tongzhi
	restaurants=Restaurant.objects.all()
	dishs=Dish.objects.all()[:8]
	if req.user.is_authenticated():
		user=req.user
		return render_to_response('index.html',locals())
	else:
		return HttpResponseRedirect('/login/')

#处理餐厅界面并处理多级查询
def restaurant(req):
	userprofiles=UserProfile.objects.all().order_by('-credit')[:5]
	notice=tongzhi
	area=req.GET.get('area',None)
	category=req.GET.get('category',None)
	grade=req.GET.get('grade',None)

	if area:
		restaurants=Restaurant.objects.filter(restaurant_area__exact=area)
		if category:
			restaurants=Restaurant.objects.filter(restaurant_category__exact=category,restaurant_area__exact=area)
	else:
		restaurants=Restaurant.objects.all()
		if category:
			restaurants=Restaurant.objects.filter(restaurant_category__exact=category)
	
	paginator=Paginator(restaurants,3)
	after_range_num=5
	before_range_num=4
	try:
		page=int(req.GET.get('page','1'))
		if page<1:
			page=1
	except ValueError:
		page=1
	try:
		comments=paginator.page(page)
	except (EmptyPage,InvalidPage,PageNotAnInteger):
		comments=paginator.page(1)
	if page >= after_range_num:
		page_range=paginator.page_range[page-after_range_num:page+before_range_num]
	else:         
		page_range=paginator.page_range[0:int(page)+before_range_num]

	if req.user.is_authenticated():
		user=req.user
		return render_to_response('restaurant.html',locals(),context_instance=RequestContext(req))
	return render_to_response('restaurant.html',locals(),context_instance=RequestContext(req))

#订餐界面，并判断从何出进入该页面并处理多级查询
def dingcan(req):
	notice=tongzhi
	category=req.GET.get('category',None)
	price=req.GET.get('price',None)

	if req.GET.get('restaurant',None):
		canting={}
		restaurant=Restaurant.objects.get(restaurant_name=req.GET['restaurant'])
		canting['name']=restaurant.restaurant_name
		canting['dizhi']=restaurant.restaurant_address
		canting=json.dumps(canting)
		dishs=Dish.objects.filter(restaurant=restaurant)
		req.session['dishs']=dishs
		if category:
			dishs=Dish.objects.filter(restaurant=restaurant,dish_category=category)
			req.session['dishs']=dishs
			if price=='big':
				dishs=Dish.objects.filter(restaurant=restaurant,dish_category=category).order_by('-dish_price')
				req.session['dishs']=dishs
			if price=='small':
				dishs=Dish.objects.filter(restaurant=restaurant,dish_category=category).order_by('dish_price')
				req.session['dishs']=dishs
		else:
			dishs=Dish.objects.filter(restaurant=restaurant)
			req.session['dishs']=dishs
			if price=='big':
				dishs=Dish.objects.filter(restaurant=restaurant).order_by('-dish_price')
				req.session['dishs']=dishs
			if price=='small':
				dishs=Dish.objects.filter(restaurant=restaurant).order_by('dish_price')
				req.session['dishs']=dishs

	else:
		if category:
			dishs=Dish.objects.filter(dish_category=category)
			req.session['dishs']=dishs
			if price=='big':
				dishs=Dish.objects.filter(dish_category=category).order_by('-dish_price')
				req.session['dishs']=dishs
			if price=='small':
				dishs=Dish.objects.filter(dish_category=category).order_by('dish_price')
				req.session['dishs']=dishs
		else:
			dishs=Dish.objects.all()
			req.session['dishs']=dishs
			if price=='big':
				dishs=Dish.objects.all().order_by('-dish_price')
				req.session['dishs']=dishs
			if price=='small':
				dishs=Dish.objects.all().order_by('dish_price')
				req.session['dishs']=dishs
	paginator=Paginator(dishs,3)
	after_range_num=5
	before_range_num=4
	try:
		page=int(req.GET.get('page','1'))
		if page<1:
			page=1
	except ValueError:
		page=1
	try:
		comments=paginator.page(page)
	except (EmptyPage,InvalidPage,PageNotAnInteger):
		comments=paginator.page(1)
	if page >= after_range_num:
		page_range=paginator.page_range[page-after_range_num:page+before_range_num]
	else:         
		page_range=paginator.page_range[0:int(page)+before_range_num]
	
	if req.user.is_authenticated():
		user=req.user
		a={}
		a['username']=user.username
		a['area']=user.get_profile().area
		a['address']=user.get_profile().address
		a['tel']=user.get_profile().tel
		users=json.dumps(a)
		return render_to_response('dingcan.html',locals(),context_instance=RequestContext(req))
	else:
		return render_to_response('dingcan.html',locals(),context_instance=RequestContext(req))

def order(req):
	global totil
	id=req.REQUEST['id']
	shu=int(req.REQUEST['shu'])
	dish=req.session['dishs'][int(id)]
	totil+=shu*dish.dish_price
	req.session['totil']=totil
	caidan=req.session['caidan']
	caidan.append(dish.dish_name)
	req.session['caidan']=(caidan)
	return HttpResponse('ok'+"<tr><td>%s</td><td>%s</td><td>%s</td><td id='qian%s'>%s</td></tr>"%(dish.dish_name,dish.dish_price,shu,id,shu*dish.dish_price))


def order_select(req):
	if req.user.is_authenticated():
		return HttpResponse('deng_select')
	else:
		return HttpResponse('no_select')

#订餐指南
def zhinan(req):
	userprofiles=UserProfile.objects.all().order_by('-credit')[:5]
	notice=tongzhi
	if req.user.is_authenticated():
		user=req.user
		return render_to_response('zhinan.html',locals())
	return render_to_response('zhinan.html',locals())

#会员中心
def show_user(req):
	global totil
	menu=''
	remark=req.GET.get('remark',None)
	mall=req.GET.get('mall',None)
	mall_obj=Mall.objects.filter(mall_name=mall)
	up_user=UserProfile.objects.get(user=req.user)
	if mall_obj:
		credit=up_user.credit-mall_obj[0].mall_credit
		print credit
		up_user.credit=credit
		order_obj=Order.objects.filter(user=req.user).order_by('-id')
		order_obj[0].mall=mall
		order_obj[0].save()

	for i in req.session['caidan']:
		menu+=','+i
	
	userprofiles=UserProfile.objects.all().order_by('-credit')[:5]
	notice=tongzhi
	if req.session['caidan']:
		Order.objects.create(menu=menu[1:],totil=totil,user=req.user,remark=remark,time=time.strftime("%Y-%m-%d %H:%M:%S"))
		credit=int(totil)+req.user.get_profile().credit
		up_user.credit=credit
		up_user.save()
		req.session['caidan']=[]
		totil=0
	orders=Order.objects.all().order_by('-id')
	if req.user.is_authenticated():
		user=req.user
		return render_to_response('show_user.html',locals())
	return render_to_response('show_user.html',locals())

#积分商城
def jifen(req):
	userprofiles=UserProfile.objects.all().order_by('-credit')[:5]
	notice=tongzhi
	malls=Mall.objects.all()
	if req.user.is_authenticated():
		user=req.user
		return render_to_response('jifen.html',locals())
	return render_to_response('jifen.html',locals())

#活动公告
def notice(req):
	userprofiles=UserProfile.objects.all().order_by('-credit')[:5]
	notices=Notice.objects.all()
	notice=tongzhi
	if req.user.is_authenticated():
		user=req.user
		return render_to_response('notice.html',locals())
	return render_to_response('notice.html',locals())

#关于我们
def women(req):
	userprofiles=UserProfile.objects.all().order_by('-credit')[:5]
	notice=tongzhi
	if req.user.is_authenticated():
		user=req.user
		return render_to_response('women.html',locals())
	return render_to_response('women.html',locals())

#招聘
def zhaopin(req):
	userprofiles=UserProfile.objects.all().order_by('-credit')[:5]
	notice=tongzhi
	if req.user.is_authenticated():
		user=req.user
		return render_to_response('zhaopin.html',locals())
	return render_to_response('zhaopin.html',locals())

#积分兑换
def duihuan(req):
	id=req.GET.get('id',None)
	if id:
		mall=Mall.objects.get(id=int(id))
	userprofiles=UserProfile.objects.all().order_by('-credit')[:5]
	notice=tongzhi
	if req.user.is_authenticated():
		user=req.user
		return render_to_response('duihuan.html',locals())
	return render_to_response('duihuan.html',locals())

#积分规则
def guize(req):
	userprofiles=UserProfile.objects.all().order_by('-credit')[:5]
	notice=tongzhi
	if req.user.is_authenticated():
		user=req.user
		return render_to_response('guize.html',locals())
	return render_to_response('guize.html',locals())

#修改密码的界面显示
def update(req):
	userprofiles=UserProfile.objects.all().order_by('-credit')[:5]
	notice=tongzhi
	if req.user.is_authenticated():
		user=req.user
		return render_to_response('update.html',locals())
	return render_to_response('update.html',locals())

#修改密码
def update_mima(req):
	if req.method=="POST":
		pwd=req.POST['new_password']
		req.user.set_password(pwd)
		req.user.save()
		logout(req)
		return HttpResponseRedirect('/login/')

#auth自带的注销功能
def user_logout(req):
	logout(req)
	return HttpResponseRedirect('/index/')
