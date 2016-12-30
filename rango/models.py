from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='priflie_images', blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    maxlength = 128
    name = models.CharField(max_length=maxlength, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Page(models.Model):
    maxlength = 128
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=maxlength)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
