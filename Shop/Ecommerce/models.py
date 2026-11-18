from django.db import models
# from django.utils.text import slagify
from django.utils.text import slugify
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

import uuid
# Create your models here.

#Create Employee model
class Employee(models.Model):
    departments = (
        ('it', 'Information Technology'),
        ('sales', 'Sales Representative'),
        ('admin', 'Adminstrator'),
        ('marketing', 'Digital Marketing')
    )

    emp_name = models.CharField(max_length=150)
    emp_email = models.EmailField(max_length=250, unique=True)
    emp_mobile = models.CharField(max_length=10, null=True, blank=True)
    emp_dept = models.CharField(max_length=100, choices=departments, default='sales')
    emp_dob = models.DateField(null=True, blank=True)
    emp_address = models.TextField(null=True, blank=True)
    emp_joining_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.emp_name


#Create Student model
class Student(models.Model):
    departments = (
        ('it', 'Information Technology'),
        ('cst', 'Computer Science Technology'),
        ('electric', 'Electrical'),
        ('ece', 'Electronics & Communication'),
        ('me', 'Mechanical'),
        ('ai', 'Artificial Inteligent'),
        ('ml', 'Machine Learning')
    )

    std_name = models.CharField(max_length=150)
    std_email = models.EmailField(max_length=250, unique=True)
    std_mobile = models.CharField(max_length=10, null=True, blank=True)
    std_dept = models.CharField(max_length=100, choices=departments, default='sales')
    std_dob = models.DateField(null=True, blank=True)
    std_address = models.TextField(null=True, blank=True)
    std_joining_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.std_name


#Creating a category table
class Category(models.Model):
    category_name=models.CharField(max_length=250,unique=True)
    category_slug=models.SlugField(null=True,blank=True)
    category_created_at=models.DateField(auto_now_add=True)

    #Override save method
    def save(self, *args, **kwargs):
        self.category_slug=slugify(self.category_name)
        return super().save()

    def __str__(self):
        return self.category_name

#Creating product table
class Product(models.Model):
    product_category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='Category')
    product_name=models.CharField(max_length=250,unique=True)
    product_slug=models.SlugField(null=True,blank=True)
    product_price=models.DecimalField(max_digits=10, decimal_places=2,default=00.00)
    product_image=models.ImageField(upload_to="products/",null=True,blank=True)
    product_desc=models.TextField()
    product_quantity_in_stock=models.IntegerField()
    product_created_at=models.DateField(auto_now_add=True)

    #Override save method
    def save(self, *args, **kwargs):
        self.product_slug=slugify(self.product_name)
        return super().save()
    
    def __str__(self):
        return self.product_name



class Favourite(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="User")
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="Product")
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}  =>  {self.product.product_slug}"



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')   # one entry per product per user
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} → {self.product.product_name} (x{self.quantity})"

    @property
    def total_price(self):
        return self.product.product_price * self.quantity



class Address(models.Model):
    ADDRESS_TYPE_CHOICES = (
        ('home', 'Home'),
        ('office', 'Office'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    
    full_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    
    address_line = models.CharField(max_length=255)   # Street / House / Building
    landmark = models.CharField(max_length=100, blank=True, null=True)
    
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    
    address_type = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPE_CHOICES,
        default='home'
    )
    
    is_default = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.city} ({self.pin_code})"



class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    # Basic Info
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    # Payment
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=(('cod','CashOnDelevery'),('online','Online')), default='cod')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL,null=True, blank=True,related_name='orders')
    # Order Status
    tracking_no = models.CharField(max_length=50, blank=True, null=True)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    razorpay_payment_id=models.CharField(max_length=250,blank=True,null=True)
    razorpay_signature=models.CharField(max_length=250,blank=True,null=True)
    razorpay_order_id=models.CharField(max_length=250,blank=True,null=True)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    
  
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_id} - {self.user.username}"


class OrderItems(models.Model):    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Important: store price at time of order
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} × {self.product.product_name}"

    @property
    def subtotal(self):
        return self.quantity * self.price