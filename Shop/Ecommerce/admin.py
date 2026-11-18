from django.contrib import admin
from Ecommerce.models import Employee
from Ecommerce.models import Student
from Ecommerce.models import *
from .models import CartItem


# Register your models here.

admin.site.register(Employee)
admin.site.register(Student)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Favourite)
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItems)