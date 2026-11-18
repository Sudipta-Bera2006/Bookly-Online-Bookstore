from django import template
from django.contrib.auth.models import User
from Ecommerce.models import Favourite
register=template.Library()

@register.simple_tag
def count_favourite_items(userid):
    user=User.objects.filter(id=userid).first()
    count=Favourite.objects.filter(user=user).count()
    return count

@register.simple_tag
def multiply_elements(a, b):
    return a*b