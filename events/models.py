from django.db import models
from django.urls import reverse

# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=255)
    short_desc = models.TextField()
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    contact_details = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='%Y/%m/%d',
                              max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=65, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:event_detail', kwargs={'slug': self.slug})

    class Meta:
        db_table = "eventapp_event"
