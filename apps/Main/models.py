from django.db import models
from django.utils import timezone


class GeneralManager(models.Model):
    is_active = models.BooleanField(default=True)

    def disable_item(self, item):
        item.is_active = False
        item.save()

    def delete_item(self, item):
        item.delete()

    class Meta:
        abstract = True


class CarouselImg(GeneralManager):
    img_carousel_url = models.ImageField(upload_to='Main/')
    img_carousel_title = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.img_carousel_title
