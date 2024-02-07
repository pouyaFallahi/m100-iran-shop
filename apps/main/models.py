from django.db import models
from django.utils import timezone
from ..User.models import User


class CarouselImg(models.Model):
    img_carousel_url = models.ImageField(upload_to='main/')
    img_carousel_title = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.img_carousel_title


class OneTimeURL(models.Model):
    url = models.CharField(max_length=256)
    is_used = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=1))
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def is_valid(self):
        return not self.is_used and timezone.now() <= self.expiry_date

    def mark_as_used(self):
        self.is_used = True
        self.save()