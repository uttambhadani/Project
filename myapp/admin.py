from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ['fname','lname','email','role']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = ['name','email','subject']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ['uid','name','category','price']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = ['uid']

@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):

    list_display = ['uid','product','pay_amount','expected_del','status']

