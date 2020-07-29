import json
from .models import *


def cookieCart(request):
    try:
        # Getting Cookie In Python Backend
        cart = json.loads(request.COOKIES["cart"])
    except:
        cart = {}

    items = []
    order = {'get_cart_items': 0, "get_cart_total": 0}
    cartItems = order["get_cart_items"]
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            # Making Total
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_items'] += cart[i]['quantity']
            order['get_cart_total'] += total

            item = {
                'product': {
                    "id": product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {"cartItems": cartItems, "order": order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        coustomer = request.user.coustomer
        order, created = Order.objects.get_or_create(
            coustomer=coustomer, complete=False)
        # will get all order item attatch to that order
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']
    return {"cartItems": cartItems, "order": order, 'items': items}


def guestOrder(request, data):

    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    coustomer, created = Coustomer.objects.get_or_create(
        email=email
    )

    coustomer.name = name
    coustomer.save()

    order = Order.objects.create(
        coustomer=coustomer,
        complete=False
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return coustomer, order
