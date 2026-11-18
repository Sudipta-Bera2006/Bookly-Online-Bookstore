from django.urls import path
from . import views

urlpatterns = [
    #Page routes
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),

    #Employees routes
    path('create_employee/', views.create_employee, name='create_employee'),
    path('employees/', views.all_employees, name='all_employees'),
    path('update_employee/<int:id>', views.update_employee, name='update_employee'),
    path('delete_employee/<int:id>', views.delete_employee, name='delete_employee'),

    #Students routes
    path('create_student/', views.create_student, name='create_student'),  
    path('students/', views.all_students, name='all_students'),
    path('update_student/<int:id>', views.update_student, name='update_student'),  
    path('delete_students/<int:id>', views.delete_student, name='delete_student'),
    
    #Authentication routes
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    #Welcome email routes
    path('welcome_email/', views.welcome_email, name='welcome_email'),


    path('product/<slug:pslug>',views.get_specific_product_details, name="get_specific_product_details"),
    path('favourites', views.get_favourite_item, name='get_favourite_item'),
    path('add/favourites/<int:pid>', views.add_to_favourites, name='add_to_favourites'),
    path('remove/favourites/<int:pid>/', views.remove_from_favourites, name='remove_from_favourites'),
    path('clear/favourites/', views.clear_favourites, name='clear_favourites'),


    path('cart/', views.get_cart_items, name='get_cart_items'),
    path('add/cart/<int:pid>/', views.add_to_cart, name='add_to_cart'),
    path('remove/cart/<int:pid>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/cart/<int:pid>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('clear/cart/', views.clear_cart, name='clear_cart'),


    path('checkout/', views.checkout, name='checkout'),
    path('checkout/process/', views.checkout_process, name='checkout_process'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),
    path('order/success/<str:tracking_no>/', views.order_success, name='order_success'),


    path('api/ai-stylist/', views.ai_stylist_chat, name='ai_stylist_chat'),



    # My Profile
    path('my-profile/', views.my_profile, name='my_profile'),

    # Change Password
    path('change-password/', views.change_password, name='change_password'),

    # Address Management
    path('add-address/', views.add_address, name='add_address'),
    path('edit-address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete_address'),

    # View Orders
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order-details/<uuid:order_id>/', views.order_details, name='order_details'),

]

