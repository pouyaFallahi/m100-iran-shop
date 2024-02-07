from django import template
from ..models import Category


register = template.Library()


@register.filter
def navbar_categories(categori):
    categories = Category.objects.all()
    return categories
