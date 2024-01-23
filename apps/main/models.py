from django.db import models


class CarouselImg(models.Model):
    img_carousel_url = models.ImageField(upload_to='apps/main/images/')
    img_carousel_title = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.img_carousel_title

