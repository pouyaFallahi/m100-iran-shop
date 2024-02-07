from django import template
from ..models import Product, Category


register = template.Library()

@register.filter
def product_image(product):
    print('product_image')
    # اولین عکس محصول را برگردانید
    if product.image.exists():
        return product.image.first().image.url
    else:
        return 'مسیر به عکس پیش‌فرض'


@register.filter
def product_images(product):
    # یک لیست از آدرس‌های تصاویر محصول بسازید
    images = product.image.all()
    for image in images:
        yield image.image.url


