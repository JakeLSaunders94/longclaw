import random
from longclaw.basket.models import BasketItem
from django.db.models import Sum

BASKET_ID_SESSION_KEY = 'basket_id'

_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'

def basket_id(request):
    if not hasattr(request, 'session'):
        request.session = {}
    if request.session.get(BASKET_ID_SESSION_KEY, '') == '':
        request.session[BASKET_ID_SESSION_KEY] = _generate_basket_id()
    return request.session[BASKET_ID_SESSION_KEY]

def _generate_basket_id():
    basket_id = ''
    for i in range(32):
        basket_id += _CHARS[random.randint(0, len(_CHARS)-1)]
    return basket_id


def get_basket_items(request):
    """
    Get all items in the basket
    """
    bid = basket_id(request)
    return BasketItem.objects.filter(basket_id=bid), bid

def get_total_basket_count(request):
    """
    Get the total number of items * quantities
    """
    bid = basket_id(request)
    sum = BasketItem.objects.filter(basket_id=bid).aggregate(Sum('quantity'))
    return sum['sum__quantity'], bid


def destroy_basket(request):
    """Delete all items in the basket
    """
    items, bid = get_basket_items(request)
    for item in items:
        item.delete()
    return bid
