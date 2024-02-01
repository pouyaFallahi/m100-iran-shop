from django import template
from ..models import Category


register = template.Library()


@register.filter
def navbar_categories(categori):
    categories = Category.objects.all()
    print('test')
    print(categories)
    return categories
