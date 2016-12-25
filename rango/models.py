from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	views=models.IntegerField(null=True)
	likes=models.IntegerField(null=True)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name


class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)

	def __unicode__(self):
		return self.title


class PageAdmin(admin.ModelAdmin):
	list_display = ('title','category','url')


class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}


class UserProfile(models.Model):
	#This line is required.Links UserProfile to a User Model instance
	user=models.OneToOneField(User)

	#The additional attriutes we wish to include
	website=models.URLField(blank=True)
	picture=models.ImageField(upload_to='profile_image',blank=True)

	#Override
	def __unicode__(self):
		return  self.user.username