# -*- coding: utf-8 -*-
import json
from django.contrib import messages
from .models import Product, Category
from django.views.generic import ListView
from django.views.generic.base import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _


def get_product_by_id(product_id):
    return get_object_or_404(Product, pk=product_id)


class ShowAllItems(ListView):
    model = Product
    template_name = 'Product/list-item.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        product = super(ShowAllItems, self).get_context_data(**kwargs)
        product['products'] = Product.objects.all()
        return product


class ShowItem(ListView):
    model = Product
    template_name = 'Product/item.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        product = super(ShowItem, self).get_context_data(**kwargs)
        product['products'] = Product.objects.get(pk=self.kwargs['pk'])
        return product


def get_cart_from_cookie(request):
    cart_data = request.COOKIES.get('cart_data', '{}')
    return json.loads(cart_data)


def add_product_to_cart(request, product_id, quantity=1):
    item_in_db = Product.objects.get(id=product_id)
    cart_data = get_cart_from_cookie(request)

    if str(product_id) in cart_data:
        total_quantity = cart_data[str(product_id)] + quantity
    else:
        total_quantity = quantity

    if item_in_db.many >= total_quantity:  # Check if the available quantity is sufficient
        if str(product_id) in cart_data:
            cart_data[str(product_id)] += quantity
        else:
            cart_data[str(product_id)] = quantity
        response = HttpResponse()
        response.set_cookie("cart_data", json.dumps(cart_data))
        print(cart_data)
        return response
    else:
        return HttpResponse("The requested quantity is not available", status=400)


def add_to_cart(request, product_id):
    return add_product_to_cart(request, product_id)


def remove_all_cart(request):
    response = HttpResponse()
    response.delete_cookie("cart_data")
    return render(request, 'Product/list-of-orders.html', context={'message': _('All items removed from cart.')})


def remove_from_cart(request, product_id):
    item_in_db = Product.objects.get(id=product_id)
    cart_data = get_cart_from_cookie(request)

    if item_in_db.many >= 0:
        if str(product_id) in cart_data:
            if cart_data[str(product_id)] > 1:
                cart_data[str(product_id)] -= 1  # Decrement the quantity by 1
            else:
                del cart_data[str(product_id)]  # Remove the product if the quantity is 1
            response = HttpResponse()
            response.set_cookie("cart_data", json.dumps(cart_data))
            return response
        else:
            return HttpResponse("The requested quantity is not available", status=400)
    else:
        return HttpResponse("The requested quantity is not available", status=400)


def show_cart_items(request):
    cart_data = get_cart_from_cookie(request)
    order_list = []
    for product_id, quantity in cart_data.items():
        product = Product.objects.get(id=product_id)
        order_list.append({
            'product_id': product_id,
            'product_name': product.name_product,
            'quantity': quantity,
            'price': product.price
        })
    return render(request, 'Product/list-of-orders.html', {'order_list': order_list})
    # return JsonResponse(order_list, safe=False) => for json


class ShowItemByCategory(View):
    model = Category
    def get(self, request, name_category):
        category = get_object_or_404(Category, name_category=name_category)
        print(category)
        products = Product.objects.filter(category=category)
        return render(request, 'Product/list-item.html', {'products': products})
