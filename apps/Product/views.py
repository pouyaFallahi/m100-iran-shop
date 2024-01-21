# -*- coding: utf-8 -*-
import json
from .models import Product
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView
from django.views.generic.base import View
from django.shortcuts import get_object_or_404, redirect


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


class RemoveFromCartView(View):

    def post(self, request):
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Product, pk=Product.id)
        cart = request.COOKIES.get('shopping_cart')
        cart = json.loads(cart) if cart else {}
        cart_item = cart.get(str(Product.id), {'quantity': 0})
        cart_item['item_id'] = Product.id
        cart_item['name'] = Product.name_product
        cart_item['price'] = Product.price
        if cart_item and cart_item['quantity'] > 0:
            cart_item['quantity'] -= 1
        cart[str(item.id)] = cart_item
        response = redirect('/coffe/')
        response.set_cookie('shopping_cart', json.dumps(cart))
        messages.success(request, f'{item.name} removed from shopping cart!')
        return response


class AddToCartView(View):
    def post(self, request):
        product_id = request.POST.get('name_product')
        print('product_id:', product_id)
        product = get_object_or_404(Product, pk=product_id)

        # از کوکی‌ها سبد خرید را دریافت یا یک واژه‌نامه خالی ایجاد کنید
        cart = json.loads(request.COOKIES.get('shopping_cart', '{}'))

        cart_item = cart.get(str(product.id), {'quantity': 0})
        cart_item['item_id'] = product.id
        cart_item['name'] = product.name_product
        cart_item['price'] = product.price
        cart_item['quantity'] += 1

        cart[str(product.id)] = cart_item

        response_data = {'message': f'{product.name_product} به سبد خرید اضافه شد!', 'cart': cart}
        response = JsonResponse(response_data)

        response.set_cookie('shopping_cart', json.dumps(cart))

        return response
