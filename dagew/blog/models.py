#coding:utf8
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	address=models.CharField(max_length=300)
	tel=models.CharField(max_length=15)
	credit=models.IntegerField()
	user=models.ForeignKey(User,unique=True)
	area=models.CharField(max_length=10)


class Notice(models.Model):
	notice_content=models.TextField()
	notice_url=models.CharField(max_length=255,blank=True)
	notice_time=models.DateField()

class Restaurant(models.Model):
	restaurant_category_choices=(
			('zs','中式餐厅'),
			('xc','西餐'),
			('rb','日本料理'),)
	restaurant_area_choices=(
			('hd','海淀'),
			('ft','丰台'),
			('cy','朝阳'),)
	restaurant_name=models.CharField(max_length=300)
	restaurant_address=models.CharField(max_length=300)
	restaurant_tel=models.CharField(max_length=15)
	restaurant_img=models.FileField(upload_to='img/')
	restaurant_category=models.CharField(max_length=2,choices=restaurant_category_choices)
	restaurant_area=models.CharField(max_length=2,choices=restaurant_area_choices)

	def __unicode__(self):
		return self.restaurant_name

class Dish(models.Model):
	dish_category_choices=(
			('xc','特色小炒'),
			('lc','精品凉菜'),
			('cs','刺身'),
			('kc','经典快餐'),
			('sc','火锅涮菜'),
			('ly','甜品冷饮'),)
	dish_name=models.CharField(max_length=300)
	dish_img=models.FileField(upload_to='img/')
	dish_category=models.CharField(max_length=2,choices=dish_category_choices)
	dish_price=models.FloatField()
#	dish_sales=models.IntegerField()
	restaurant=models.ForeignKey(Restaurant)
	
	def __unicode__(self):
		return self.dish_name

class Order(models.Model):
	menu=models.TextField()
	totil=models.FloatField()
	remark=models.CharField(max_length=300,blank=True)
	time=models.DateTimeField()
	mall=models.CharField(max_length=255,blank=True)
	user=models.ForeignKey(User)

class Mall(models.Model):
	mall_name=models.CharField(max_length=50)
	mall_img=models.FileField(upload_to='img/')
	mall_credit=models.IntegerField()

	def __unicode__(self):
		return self.mall_name
