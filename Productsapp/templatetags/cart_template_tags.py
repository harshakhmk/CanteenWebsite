from django import template
from ..models import *

register = template.Library()
@register.filter
def cart_items_count(user):
    if user.is_authenticated():
        order_qs=Order.objects.filter(user=user.customer,is_complete=False)
        if order_qs.exists():
            order=order_qs[0]
            return order.products.count()

    return 0        