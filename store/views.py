from django.shortcuts import render
from .models import *
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
    context = {}
    return render(request, "store/checkout.html", context)
