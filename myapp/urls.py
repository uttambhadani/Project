from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about, name='about'),
    path('abc/',views.abc, name='abc'),
    path('contact/',views.contact, name='contact'),
    path('register/',views.register, name='register'),
    path('otp/',views.otp, name='otp'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('forgot-pass/',views.forgot_pass, name='forgot-pass'),
    path('profile/',views.profile, name='profile'),
    path('add-product/',views.add_product, name='add-product'),
    path('seller-product/',views.seller_product, name='seller-product'),
    path('edit-product/<int:pk>',views.edit_product, name='edit-product'),
    path('delete-product/<int:pk>',views.delete_product, name='delete-product'),
    path('all-product/',views.all_product, name='all-product'),
    path('view-product/<int:pk>',views.view_product, name='view-product'),
    path('add-to-cart/<int:pk>',views.add_to_cart,name='add-to-cart'),
    path('view-cart/',views.view_cart,name='view-cart'),
    path('delete-cart/<int:pk>',views.delete_cart,name='delete-cart'),
    path('buy-product/<int:pk>',views.buy_product,name='buy-product'),
    # path('order-confirm/', views.order_confirm, name='order-confirm'),
    path('buy-product/paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('seller-buy-product/', views.seller_buy_product, name='seller-buy-product'),
    path('view-buy-product/<int:pk>', views.view_buy_product, name='view-buy-product'),
    path('complete-del/<int:pk>', views.complete_del, name='complete-del'),

]