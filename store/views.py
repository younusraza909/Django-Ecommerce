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
        items = order.orderitem_set.all()
    else:
        items = []
    context = {"items": items}
    return render(request, "store/cart.html", context)


def checkout(request):
    context = {}
    return render(request, "store/checkout.html", context)
