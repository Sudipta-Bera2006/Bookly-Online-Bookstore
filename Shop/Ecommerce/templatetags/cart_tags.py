from django import template
from Ecommerce.models import CartItem, Favourite   # change Ecommerce to your app name

register = template.Library()


@register.simple_tag
def count_cart_items(user_id):
    if user_id:
        return CartItem.objects.filter(user_id=user_id).count()
    return 0


@register.simple_tag
def count_favourite_items(user_id):
    if user_id:
        return Favourite.objects.filter(user_id=user_id).count()
    return 0