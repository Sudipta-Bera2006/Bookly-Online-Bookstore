from django.shortcuts import render,redirect
from django.http import HttpResponse
from Ecommerce.models import Employee
from Ecommerce.models import Student
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from Ecommerce.helper import custom_mail
from django.contrib.auth.decorators import login_required
from Ecommerce.models import *
from django.shortcuts import render, get_object_or_404
from .models import *   # make sure Product model is imported
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models import Q
from .models import Product, Category
import razorpay
from django.conf import settings
#setup mrezorpay client
client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
from django.views.decorators.http import require_GET, require_POST
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .ai_services import get_ai_stylist_recommendation
from django.contrib.auth import update_session_auth_hash
from .models import Address
# Create your views here.

@login_required(login_url='user_login')
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


def shop(request):
    products = Product.objects.select_related("product_category").all()
    categories = Category.objects.all()

    # Search
    search_query = request.GET.get("q", "").strip()

    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) |
            Q(product_desc__icontains=search_query) |
            Q(product_category__category_name__icontains=search_query)
        )

    # Category filter
    category_id = request.GET.get("category", "").strip()

    if category_id:
        products = products.filter(product_category_id=category_id)

    # Sorting
    sort_by = request.GET.get("sort", "").strip()

    if sort_by == "price_low":
        products = products.order_by("product_price")

    elif sort_by == "price_high":
        products = products.order_by("-product_price")

    elif sort_by == "name":
        products = products.order_by("product_name")

    elif sort_by == "newest":
        products = products.order_by("-product_created_at")

    context = {
        "products": products,
        "categories": categories,
        "search_query": search_query,
        "selected_category": category_id,
        "selected_sort": sort_by,
    }

    return render(request, "shop.html", context)

def blog(request):
    return render(request, 'blog.html')

def contact(request):
    return render(request, 'contact.html')


@login_required(login_url='user_login')
def create_employee(request):
    if request.method=="POST":
        emp_name=request.POST['emp_name']
        emp_email=request.POST['emp_email']
        emp_mobile=request.POST['emp_mobile']
        emp_dept=request.POST['emp_dept']
        emp_dob=request.POST['emp_dob']
        emp_address=request.POST['emp_address']

        try :
            emp_obj=Employee.objects.create(
                emp_name=emp_name,
                emp_email=emp_email,
                emp_mobile=emp_mobile,
                emp_dept=emp_dept,
                emp_dob=emp_dob,
                emp_address=emp_address
            )
            if emp_obj:
                messages.success(request,f"New employee created ! {emp_name}")
                return redirect("create_employee")
            else:
                messages.error(request,f"Employee not created ! {emp_name}")
                return redirect("create_employee")
        except Exception as e:
            messages.success(request,f"Error : {e}")
            return redirect("create_employee")
    return render(request,'create_employee.html')


@login_required(login_url='user_login')
def all_employees(request):
    emps=Employee.objects.all()
    payload={
        'emps':emps
    }
    return render(request,"all_employees.html",payload)


@login_required(login_url='user_login')
def update_employee(request, id):
    emp=None
    try:
        emp=Employee.objects.filter(id=id).first()
    except Exception as e:
        messages.error(request,f"Error : {e}")
        return redirect("all_employees")


    if request.method == "POST":
        emp_name=request.POST['emp_name']
        emp_mobile=request.POST['emp_mobile']
        emp_dept=request.POST['emp_dept']
        emp_dob=request.POST['emp_dob']
        emp_address=request.POST['emp_address']

        emp.emp_name=emp_name
        emp.emp_mobile=emp_mobile
        emp.emp_dept=emp_dept
        emp.emp_dob=emp_dob
        emp.emp_address=emp_address
        emp.save()

        messages.success(request,f"Employee update successfully !")
        return redirect("all_employees")

    payload={
        'id' : id,
        'emp' : emp
    }
    return render(request,'update_employee.html',payload)

@login_required(login_url='user_login')
def delete_employee(request, id):
    try:
        emp=Employee.objects.filter(id=id).first()
        emp.delete()
        messages.success(request,f"Employee deleted successfully !")
        return redirect("all_employees")
    except Exception as e:
        messages.error(request,f"Error : {e}")
        return redirect("all_employees")


@login_required(login_url='user_login')
def create_student(request):
    if request.method=="POST":
        std_name=request.POST['std_name']
        std_email=request.POST['std_email']
        std_mobile=request.POST['std_mobile']
        std_dept=request.POST['std_dept']
        std_dob=request.POST['std_dob']
        std_address=request.POST['std_address']


        try :
            std_obj=Student.objects.create(
                std_name=std_name,
                std_email=std_email,
                std_mobile=std_mobile,
                std_dept=std_dept,
                std_dob=std_dob,
                std_address=std_address
            )

            if std_obj:
                messages.success(request,f"New student created ! {std_name}")
                return redirect("create_student")
            else:
                messages.error(request,f"Student not created ! {std_name}")
                return redirect("create_student")
        except Exception as e:
            messages.success(request,f"Error : {e}")
            return redirect("create_employee")
    return render(request,'create_student.html')


@login_required(login_url='user_login')
def all_students(request):
    stds=Student.objects.all()
    payload={
        'stds':stds
    }
    return render(request,"all_students.html",payload)


@login_required(login_url='user_login')
def update_student(request, id):
    std=None
    try:
        std=Student.objects.filter(id=id).first()
    except Exception as e:
        messages.error(request,f"Error : {e}")
        return redirect("all_students")

    if request.method == "POST":
        std_name=request.POST['std_name']
        std_mobile=request.POST['std_mobile']
        std_dept=request.POST['std_dept']
        std_dob=request.POST['std_dob']
        std_address=request.POST['std_address']

        std.std_name=std_name
        std.std_mobile=std_mobile
        std.std_dept=std_dept
        std.std_dob=std_dob
        std.std_address=std_address
        std.save()

        messages.success(request,f"Student update successfully !")
        return redirect("all_students")
    
    payload={
        'id' : id,
        'std' : std
    }
    return render(request,'update_student.html',payload)


@login_required(login_url='user_login')
def delete_student(request, id):
    try:
        std=Student.objects.filter(id=id).first()
        std.delete()
        messages.success(request,f"Student deleted successfully !")
        return redirect("all_students")
    except Exception as e:
        messages.error(request,f"Error : {e}")
        return redirect("all_students")




'''
Authentication
'''
def user_register(request):
    if request.method == "POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['user_name']
        password=request.POST['password']

        try:
            User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=make_password(password)
            )
            body_message=f'''
                Subject:Confirming your registration
                Hi {first_name},
                Thank you for registering an account with [Bookly]. We are thrilled to have you join our community!
                Your account has been successfully created. You can now log in to explore our features, manage your profile, and access your dashboard.
                Your Account Details:
                    • Username/Email: {username}
                Quick Next Steps:
                    • Complete your profile: Fill out your preferences to get a personalized experience.
                    • Explore resources: Check out our [Getting Started Guide / Help Center] to learn the basics.
                    • Get support: If you ever run into issues, visit our support page or reply directly to this email.
                Best regards,
                The [Bookly] Team
'''
            custom_mail(title="hey, Welcome to Bookly store", message=body_message, receptients=[email])
            messages.success(request,f"New user register !")
            return redirect("user_register")
        except Exception as e:
            messages.error(request,f"Error : {e}")
            return redirect("user_register")

    return render(request,'Auth/user_register.html')

def user_login(request):
    if request.method=="POST":
        username=request.POST['user_name']
        password=request.POST['password']

        try:
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect("shop")
            else:
                messages.error(request,f"Raised essue during login !")
                return redirect("user_login")
        except Exception as e:
            messages.error(request,f"Error : {e}")
            return redirect("user_login")

    return render(request,'Auth/user_login.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')

def welcome_email(request):
    try:
        send_mail(
            'Welcome to our shop!',
            'Thank you for registering.',
            'sudiptabera802@gmail.com',            # uses DEFAULT_FROM_EMAIL
            ['sudiptabera802@gmail.com'],
            fail_silently=False,
        )
    except Exception as e:
        print("Error : ",e)

    return HttpResponse("Email send")






def get_specific_product_details(request, pslug):
    product=None
    try:
        product=Product.objects.filter(product_slug=pslug).first()
    except Exception as e:
        print("Error: ",e)

    payload={
        'product' : product
    }
    return render(request, "specific_product.html", payload)



def get_favourite_item(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    favourite_items = Favourite.objects.filter(
        user=request.user
    ).select_related('product')

    favourite_count = favourite_items.count()

    payload = {
        "favourite_items": favourite_items,
        "favourite_count": favourite_count,
    }

    return render(request, "favourite_items.html", payload)


def add_to_favourites(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')

    product = get_object_or_404(Product, id=pid)

    # Avoid adding the same product repeatedly
    Favourite.objects.get_or_create(
        user=request.user,
        product=product,
    )

    return redirect('get_favourite_item')


def remove_from_favourites(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')

    # Delete all duplicate records for this user and product
    Favourite.objects.filter(
        user=request.user,
        product_id=pid,
    ).delete()

    return redirect('get_favourite_item')


def clear_favourites(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    Favourite.objects.filter(
        user=request.user
    ).delete()

    return redirect('get_favourite_item')



def get_cart_items(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    total_amount = sum(item.total_price for item in cart_items)
    cart_count = cart_items.count()

    context = {
        'cart_items': cart_items,
        'cart_count': cart_count,
        'total_amount': total_amount,
    }
    return render(request, 'cart_items.html', context)   # change template name if needed


def add_to_cart(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    product = get_object_or_404(Product, id=pid)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('get_cart_items')


def remove_from_cart(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    cart_item = get_object_or_404(CartItem, user=request.user, product_id=pid)
    cart_item.delete()
    return redirect('get_cart_items')


def update_cart_quantity(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, user=request.user, product_id=pid)

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('get_cart_items')


def clear_cart(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    CartItem.objects.filter(user=request.user).delete()
    return redirect('get_cart_items')

def checkout(request):
    current_user=request.user
    total=0
    cart_items=CartItem.objects.filter(user=current_user)
    for i in cart_items:
        total += i.product.product_price * i.quantity

    address = Address.objects.filter(user = current_user)
    payload={
        'cart_items' : cart_items,
        'total': total,
        'address' : address
    }
    return render(request, 'checkout.html', payload)




def checkout_process(request):
    total = 0
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)

    for i in cart_items:
        total += i.product.product_price * i.quantity

    if request.method == "POST":
        address_id = request.POST.get('address')
        payment_type = request.POST.get('payment')

        if not address_id:
            return HttpResponse("Please select a shipping address.")

        address = Address.objects.filter(id=address_id, user=current_user).first()
        if not address:
            return HttpResponse("Invalid address selected.")

        if payment_type == "cod":
            order_obj = Order.objects.create(
                user=current_user,
                payment_method='cod',
                address=address,
                payment_amount=total,
                payment_status='pending',
            )

            order_obj.tracking_no = f"ORD-{str(order_obj.pk)[:8].upper()}"
            order_obj.save()

            for item in cart_items:
                OrderItems.objects.create(
                    order=order_obj,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.product_price
                )

            cart_items.delete()

            # Pass the order object so the template can display the data
            return render(request, "order_success.html", {
                "order_details": order_obj
            })
        # In COD block:
            return redirect('order_success', tracking_no=order_obj.tracking_no)
        elif payment_type == "upi":
            razorpay_amount = int(total * 100)

            razorpay_order = client.order.create({
                'amount': razorpay_amount,
                'currency': 'INR',
                'payment_capture': 1
            })

            # Create order but DO NOT empty the cart yet
            order = Order.objects.create(
                user=current_user,
                payment_method='online',
                address=address,
                payment_amount=total,
                razorpay_order_id=razorpay_order['id'],
                payment_status='pending',
            )

            # Generate tracking number
            # order.tracking_no = f"ORD{order.id:06d}"
            order.tracking_no = f"ORD-{str(order.pk)[:8].upper()}"

            order.save()

            for item in cart_items:
                OrderItems.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.product_price
                )

            # ← Cart is NOT deleted here

            payload = {
                'order': order,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': razorpay_amount,
                'currency': 'INR',
            }
            return render(request, 'rzr_checkout.html', payload)

        else:
            return HttpResponse(f"Unknown payment method received: {payment_type}")

    return HttpResponse("Checkout processing....")








@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')

        order = Order.objects.filter(razorpay_order_id=razorpay_order_id).first()
        if not order:
            messages.error(request, "Order not found.")
            return redirect('checkout')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)

            # Success
            order.payment_status = 'success'
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.save()

            # Empty cart only after successful verification
            CartItem.objects.filter(user=order.user).delete()

            messages.success(request, "Payment successful! Your order has been placed.")
            payload={
                'order_details' : order
            }
            return render(request, 'order_success.html', payload)

        except razorpay.errors.SignatureVerificationError:
            order.payment_status = 'Failed'
            order.save()
            messages.error(request, "Payment verification failed. Please try again.")
            return redirect('checkout')

    return redirect('checkout')



# def order_success(request):
#     return redirect(request,'order_success.html')


def order_success(request, tracking_no):
    order = get_object_or_404(Order, tracking_no=tracking_no, user=request.user)
    return render(request, "order_success.html", {
        "order_details": order
    })






@require_POST
def ai_stylist_chat(request):
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()

        if not user_message:
            return JsonResponse({"error": "Prompt cannot be empty"}, status=400)

        # Pass the real user object (can be AnonymousUser)
        ai_reply = get_ai_stylist_recommendation(
            user_prompt=user_message,
            user=request.user,
        )
        return JsonResponse({"reply": ai_reply})

    except Exception as e:
        print(f"[ai_stylist_chat] {e}")
        return JsonResponse({"error": str(e)}, status=500)




from .forms import (
    UserProfileForm,
    AddressForm,
    CustomPasswordChangeForm
)




# ==========================
# MY PROFILE
# ==========================

@login_required
def my_profile(request):

    if request.method == 'POST':

        form = UserProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            updated_user = form.save()

            messages.success(
                request,
                'Your profile has been updated successfully!'
            )

            return redirect('my_profile')

        else:

            messages.error(
                request,
                'Please correct the errors below.'
            )

    else:

        form = UserProfileForm(
            instance=request.user
        )

    addresses = Address.objects.filter(
        user=request.user
    )

    return render(
        request,
        'my_profile.html',
        {
            'form': form,
            'addresses': addresses
        }
    )


# ==========================
# CHANGE PASSWORD
# ==========================
@login_required
def change_password(request):

    if request.method == 'POST':

        form = CustomPasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                'Your password has been changed successfully!'
            )

            return redirect('my_profile')

        else:

            messages.error(
                request,
                'Password could not be changed. Check the errors below.'
            )

    else:

        form = CustomPasswordChangeForm(
            user=request.user
        )

    return render(
        request,
        'change_password.html',
        {
            'form': form
        }
    )

# ==========================
# ADD ADDRESS
# ==========================

@login_required
def add_address(request):

    if request.method == 'POST':

        form = AddressForm(request.POST)

        if form.is_valid():

            address = form.save(commit=False)
            address.user = request.user

            if address.is_default:
                Address.objects.filter(
                    user=request.user
                ).update(is_default=False)

            address.save()

            messages.success(
                request,
                'Address added successfully!'
            )

            return redirect('my_profile')

    else:

        form = AddressForm()

    return render(
    request,
    'address_form.html',
    {
        'form': form,
        'title': 'Add New Address'
    }
)


# ==========================
# EDIT ADDRESS
# ==========================


@login_required
def edit_address(request, address_id):

    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    if request.method == 'POST':

        form = AddressForm(
            request.POST,
            instance=address
        )

        if form.is_valid():

            updated_address = form.save(commit=False)

            if updated_address.is_default:
                Address.objects.filter(
                    user=request.user
                ).exclude(
                    id=address.id
                ).update(is_default=False)

            updated_address.save()

            messages.success(
                request,
                'Address updated successfully!'
            )

            return redirect('my_profile')

    else:

        form = AddressForm(instance=address)

    return render(
        request,
        'address_form.html',
        {
            'form': form,
            'title': 'Update Address'
        }
    )



# ==========================
# DELETE ADDRESS
# ==========================

@login_required
def delete_address(request, address_id):

    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    if request.method == 'POST':

        address.delete()

        messages.success(
            request,
            'Address deleted successfully!'
        )

    return redirect('my_profile')


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    context = {
        'orders': orders,
    }

    return render(
        request,
        'my_orders.html',
        context
    )



@login_required
def order_details(request, order_id):

    order = get_object_or_404(
        Order.objects.prefetch_related(
            'orderitems_set__product'
        ),
        order_id=order_id,
        user=request.user
    )

    order_items = order.orderitems_set.all()

    return render(
        request,
        'order_details.html',
        {
            'order': order,
            'order_items': order_items
        }
    )
