# -*- coding: utf-8 -*-
from random import randint
from .models import OneTimeURL
from .models import CarouselImg
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from ..Product.models import Category, Product
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist


def carousel_view(request):
    carousel_img = CarouselImg.objects.all()
    return render(request, 'home-page.html', {'carousel_img': carousel_img})


def generate_one_time_url(request):
    # ایجاد URL یک بار مصرف
    url_id = randint(100000, 999999)
    one_time_url = OneTimeURL.objects.create(url=url_id, expiry_date=timezone.now() + timezone.timedelta(days=1))

    data = {
        'url_id': one_time_url.id,
        'url': request.bild_absolute_uri(url_id + str(one_time_url.url) + '/'),
        'expiry_date': str(one_time_url.expiry_date),
    }
    return JsonResponse(data)


def use_one_time_url(request, url_id):
    # بررسی و استفاده از URL یک بار مصرف
    try:
        one_time_url = OneTimeURL.objects.get(id=url_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'URL not found'}, status=404)

    if one_time_url.is_valid():
        # انجام عملیات مورد نظر با استفاده از این URL
        # مانند تغییر رمز عبور، تایید ایمیل و ...
        one_time_url.mark_as_used()
        return JsonResponse({'success': 'URL used successfully'}, status=200)
    else:
        return JsonResponse({'error': 'URL is not valid or expired'}, status=400)



