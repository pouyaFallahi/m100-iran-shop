from django.contrib import admin
from ..Product.models import Product, Company, Category
from ..User.models import User

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Company)
admin.site.register(Category)