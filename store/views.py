from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
# this decorator tells django that we dont need csrf token to send data to this view
# from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def store(request):
    if request.user.is_authenticated:
        coustomer = request.user.coustomer
        order, created = Order.objects.get_or_create(
            coustomer=coustomer, complete=False)
        # will get all order item attatch to that order
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, "get_cart_total": 0}
        cartItems = order["get_cart_items"]
    products = Product.objects.all()
    context = {"products": products, "cartItems": cartItems, "shipping": False}
    return render(request, "store/store.html", context)


def cart(request):
    if request.user.is_authenticated:
        coustomer = request.user.coustomer
        order, created = Order.objects.get_or_create(
            coustomer=coustomer, complete=False)
        # will get all order item attatch to that order
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, "get_cart_total": 0}
        cartItems = order["get_cart_items"]
    context = {"items": items, "order": order,
               "cartItems": cartItems, "shipping": False}
    return render(request, "store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        coustomer = request.user.coustomer
        order, created = Order.objects.get_or_create(
            coustomer=coustomer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, "get_cart_total": 0, "shipping": False}
        cartItems = order["get_cart_items"]
    context = {"items": items, "order": order, "cartItems": cartItems}
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

# this decorator tells django that we dont need csrf token to send data to this view
# @csrf_exempt


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if (request.user.is_authenticated):
        coustomer = request.user.coustomer
        order, created = Order.objects.get_or_create(
            coustomer=coustomer, complete=False)
        total = float(data["form"]['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingModel.objects.create(
                coustomer=coustomer,
                order=order,
                address=data["shipping"]["address"],
                city=data["shipping"]["city"],
                states=data["shipping"]["state"],
                zipcode=data["shipping"]["zipcode"]
            )
            print("Model Created For Shippment")
    else:
        print("User Not Logged In")
    return JsonResponse("payment Submitted", safe=False)
