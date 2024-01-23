from django.contrib import admin
from ..Product.models import Product, Company, Category
from ..User.models import User
from .models import CarouselImg

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Company)
admin.site.register(Category)
admin.site.register(CarouselImg)
