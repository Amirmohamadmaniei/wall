from django.db import models
from django.conf import settings


class AD(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=170)
    description = models.TextField()

    tell = models.CharField(max_length=11)
    price = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    ad = models.ForeignKey(AD, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='AD/')

    def __str__(self):
        return self.ad.title
