from django.db import models
from django.utils import timezone
from django.urls import reverse
from filer.fields.image import FilerImageField
from ckeditor.fields import RichTextField
# Create your models here.
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):
	name = models.CharField(max_length=200,db_index=True)
	slug = models.SlugField(max_length=200,db_index=True,unique=True)
	

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'


	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('toptran:product_list_by_category',args=[self.slug])

   


@python_2_unicode_compatible
class Product(models.Model):
	category = models.ForeignKey(Category,related_name='products')

	name = models.CharField(max_length=200,db_index=True)
	slug = models.SlugField(max_length=200,db_index=True)
	image = FilerImageField(null=True,blank=True,related_name='products_image')
	description = RichTextField(blank=True,null=True,verbose_name="description")
	


	class Meta:
		ordering = ('name',)
		index_together = (('id','slug'),)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('toptran:product_detail',args=[self.id,self.slug])



@python_2_unicode_compatible
class News(models.Model):
	image = FilerImageField(null=True,blank=True,related_name='news_image')
	title = models.CharField(max_length=200)
	body = RichTextField(blank=True,null=True,verbose_name="body")
	pub_date = models.DateTimeField(default=timezone.now)
	views = models.PositiveIntegerField(default=0)


	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])
   


	class Meta():
		ordering = ['-pub_date']

	def __str__(self):
		return self.title

	# 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数

	def get_absolute_url(self):
		return reverse('toptran:newsdetail', kwargs={'pk': self.pk})


@python_2_unicode_compatible
class Case(models.Model):
	image = FilerImageField(null=True,blank=True,related_name='case_image')

@python_2_unicode_compatible
class Index(models.Model):
	image = FilerImageField(null=True,blank=True,related_name='index_image')

	

@python_2_unicode_compatible
class Knowledge(models.Model):
	image = FilerImageField(null=True,blank=True,related_name='knowledge_image')
	title = models.CharField(max_length=200)
	body = RichTextField(blank=True,null=True,verbose_name="body")
	pub_date = models.DateTimeField(default=timezone.now)
	views = models.PositiveIntegerField(default=0)


	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])
   


	class Meta():
		ordering = ['-pub_date']

	def __str__(self):
		return self.title

	# 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数

	def get_absolute_url(self):
		return reverse('toptran:knowledgedetail', kwargs={'pk': self.pk})