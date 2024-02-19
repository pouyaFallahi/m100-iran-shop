from django import template
from ..models import Category, Company


register = template.Library()


@register.filter
def navbar_categories(categori):
    categories = Category.objects.all()
    return categories

@register.filter
def show_company(company):
    company = Company.objects.all()
    return company
