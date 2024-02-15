import json
from django.shortcuts import render
from ..Product.models import Product
from .models import CartItem
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.translation import gettext_lazy as _
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import status




@api_view(['GET', 'POST', 'DELETE'])
def add_remove_item_cart_to_cookie(request: Request, pk):
    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        product_serializer = ProductSerializer(product)
        return Response(product_serializer.data)

    elif request.method == 'POST':
        try:
            product = Product.objects.get(pk=pk)
            if 'item_cart' in request.COOKIES:
                item_cart = json.loads(request.COOKIES['item_cart'])
            else:
                item_cart = {}

            if str(product.id) in item_cart:
                if product.many > item_cart[str(product.id)]:
                    item_cart[str(product.id)] += 1
                else:
                    return Response(None, status.HTTP_400_BAD_REQUEST)
            else:
                item_cart[str(product.id)] = 1
            response = Response(None, status=status.HTTP_201_CREATED)
            response.set_cookie('item_cart', json.dumps(item_cart), expires=24 * 60 * 60)
            return response
        except Product.DoesNotExist:
            return Response(None, status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        if 'item_cart' in request.COOKIES:
            item_cart = json.loads(request.COOKIES['item_cart'])
            if item_cart[str(pk)] > 0:
                item_cart[str(pk)] -= 1
                response = Response(None, status=status.HTTP_204_NO_CONTENT)
                response.set_cookie('item_cart', json.dumps(item_cart))
                return response
            elif item_cart[str(pk)] < 0:
                Response(None, status=status.HTTP_204_NO_CONTENT)


def get_cart_from_cookie(request):
    cart_data = request.cookie.get('item_cart', '{}')
    return json.loads(cart_data)


def show(request):
    cart_data = request
    print(f'data is: {cart_data}')
    return render(request, 'Product/list-of-orders.html', context={'message': _('All items removed from cart.')})



