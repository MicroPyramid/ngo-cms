from django.db import models
import datetime
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=65, unique=True)
    image = models.ImageField(upload_to='%Y/%m/%d',
                              max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "blogapp_category"

class Gal_Image(models.Model):
    image = models.ImageField(upload_to='%Y/%m/%d',
                              max_length=255, null=True, blank=True)

    class Meta:
        db_table = "blogapp_gal_image"


class Post(models.Model):
    title = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    short_desc = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='%Y/%m/%d')
    is_featured_news = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    photos = models.ManyToManyField(Gal_Image, blank=True)
    slug = models.SlugField(max_length=65, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    class Meta:
        db_table = "blogapp_post"


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "blogapp_contact"


class Menu(models.Model):
    name = models.CharField(max_length=30, unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    slug = models.CharField(max_length=65, unique=True)
    lvl = models.IntegerField()

    class Meta:
        db_table = "blogapp_menu"


class Page(models.Model):
    title = models.CharField(max_length=65, unique=True)
    content = models.TextField()
    photos = models.ManyToManyField(Gal_Image, blank=True)
    slug = models.SlugField(max_length=65, unique=True)

    class Meta:
        db_table = "blogapp_page"


class Image_File(models.Model):
    upload = models.FileField(upload_to="uploads/%Y/%m/%d/")
    date_created = models.DateTimeField(default=datetime.datetime.now)
    is_image = models.BooleanField(default=True)
    thumbnail = models.FileField(
        upload_to="uploads/%Y/%m/%d/", blank=True, null=True)

    class Meta:
        db_table = "blogapp_image_file"


class Banner(models.Model):
    title = models.CharField(max_length=155, unique=True)
    image = models.ImageField(upload_to='%y/%m/%d')
    short_desc = models.TextField(blank=True, null=True)


    class Meta:
        db_table = "blogapp_banner"