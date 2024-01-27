from ..User.models import User
from .models import CarouselImg
from django.contrib import admin
from ..Product.models import Product, Company, Category, ImageForProduct

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Company)
admin.site.register(Category)
admin.site.register(CarouselImg)
admin.site.register(ImageForProduct)
