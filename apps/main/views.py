# -*- coding: utf-8 -*-
from .models import CarouselImg
from ..Product.models import Category
from django.shortcuts import render
from django.views.generic import ListView


def carousel_view(request):
    carousel_img = CarouselImg.objects.all()
    category = Category.objects.all()
    print(category.values())
    return render(request, 'home-page.html', {'carousel_img': carousel_img, 'category': category})


