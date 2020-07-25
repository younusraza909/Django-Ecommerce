from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

# Create your views here.


def store(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "store/store.html", context)


def cart(request):
    if request.user.is_authenticated:
        coustomer = request.user.coustomer
        order, created = Order.objects.get_or_create(
            coustomer=coustomer, complete=False)
        # will get all order item attatch to that order
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items': 0, "get_cart_total": 0}
    context = {"items": items, "order": order}
    return render(request, "store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        coustomer = request.user.coustomer
        order, created = Order.objects.get_or_create(
            coustomer=coustomer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items': 0, "get_cart_total": 0}
    context = {"items": items, "order": order}
    return render(request, "store/checkout.html", context)


def update_item(request):
    # to parse data from json in phython
    data = json.loads(request.body)
    productId = data['productId']
    action = data["action"]
    print("Action", action)
    print("Product", productId)

    coustomer = request.user.coustomer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        coustomer=coustomer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    if action == "add":
        orderItem.quantity = (orderItem.quantity+1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity-1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item Was Added", safe=False)
