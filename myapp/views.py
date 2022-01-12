from typing import TextIO
from django.db.models.fields import UUIDField
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randrange,choices
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from datetime import date


# Create your views here.

def index(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        return render(request,'index.html',{'uid':uid})
    except:
        return render(request,'index.html')





def about(request):
    return render(request,'about.html')

def abc(request):
    return render(request,'abc.html')


def contact(request):
    if request.method == 'POST':
        Contact.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            subject = request.POST['subject'],
            message = request.POST['message']
        )
        subject = 'Thank You from E-Comm'
        message = f'Hello {request.POST["name"]}! Thank you for Contact us. Admin will contact you soon.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.POST['email'], ]
        send_mail( subject, message, email_from, recipient_list )

        subject = 'Some one is Contacting you'
        message = f"""Hello Admin! Someone is tring to contactr you HEre are the details as follow : 
                NAme : {request.POST['name']}
                email : {request.POST['email']}
                subject : {request.POST['subject']}
                message :  {request.POST['message']}"""
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['email.ecomm6@gmail.com', ]
        send_mail( subject, message, email_from, recipient_list )

        return render(request,'contact.html',{'msg':'Will Contact you soon.'})
    return render(request,'contact.html')

def register(request):
    if request.method == 'POST':
        try:
            User.objects.get(email=request.POST['email'])
            msg = 'Your Email already Exist'
            return render(request,'register.html',{'msg':msg})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                global temp
                otp = randrange(1000,9999)

                temp = {
                    'fname' : request.POST['fname'],
                    'lname' : request.POST['lname'],
                    'email' : request.POST['email'],
                    'mobile' : request.POST['mobile'],
                    'address' : request.POST['address'],
                    'role' : request.POST['role'],
                    'password' : request.POST['password'],
                    'otp' : otp
                }
                subject = 'Ecomm OTP verify'
                message = f'Hello User your OTP is  : {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'otp.html',{'otp':otp})

            else: 
                msg = 'Password and confirm Password does not match'
                return render(request,'register.html',{'msg':msg})


    return render(request,'register.html')

def otp(request):
    if request.method == "POST":
        if request.POST['otp'] == request.POST['uotp']:
            global temp
            User.objects.create(
                fname = temp['fname'],
                lname = temp['lname'],
                email = temp['email'],
                mobile = temp['mobile'],
                address = temp['address'],
                role = temp['role'],
                password = temp['password'],
            )
            msg = 'User created'
            del temp
            return render(request,'register.html',{'msg':msg})
        else:
            msg = 'OTP does not match'
            return render(request,'otp.html',{'msg':msg,'otp':request.POST['otp']})
        
    return render(request,'otp.html')


def login(request):
    if request.method == 'POST':
        try:
            uid = User.objects.get(email=request.POST['email'])
            if request.POST['password'] == uid.password:
                request.session['email'] = request.POST['email']
                return render(request,'index.html',{'uid':uid})
            else:
                return render(request,'login.html',{'msg':'INcorrect Password'})
                

        except:
            msg = 'Go and Register first'
            return render(request,'login.html',{'msg':msg})

    return render(request,'login.html')

def logout(request):
    del request.session['email']
    return redirect('index')

def forgot_pass(request):
    if request.POST:
        try:
            uid = User.objects.get(email=request.POST['email'])
            s = 'QWERTYUIOPLKJHGFDSAqwertyuioplkjhgfdsa1236547889'
            pw = ''.join(choices(s,k=8))
            subject = 'Ecomm Rerset title'
            message = f"""Hello {uid.fname}  {uid.lname}!!, 
            Your old password is : {uid.password}
            Your New Password is : {pw}
            
            **Please Login with New Password"""
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )
            uid.password = pw
            uid.save()
            return render(request,'login.html',{'msg':'New password is sent on your email'})
        except:
            return render(request,'forgot-pass.html',{'msg':'Email is not register'})

    return render(request,'forgot-pass.html')


def profile(request):
    uid = User.objects.get(email=request.session['email'])

    if request.method == 'POST':
        if request.POST['password'] == request.POST['cpassword']:
            uid.fname = request.POST['fname']
            uid.lname = request.POST['lname']
            uid.mobile = request.POST['mobile']
            uid.address = request.POST['address']
            uid.password = request.POST['password']
            uid.save()
            return redirect('profile')
        else:
            return render(request,'profile.html',{'msg':'Password and Confirm Password does not match','uid':uid})

    return render(request,'profile.html',{'uid':uid})


def add_product(request):
    uid = User.objects.get(email= request.session['email'])
    if request.method == 'POST':
        # if 'pic' in request.FILES
        Product.objects.create(
            uid = uid,
            name = request.POST['name'],
            price = request.POST['price'],
            quantity = request.POST['quantity'],
            category = request.POST['category'],
            pic = request.FILES['pic']
        )
        return render(request,'add-product.html',{'uid':uid,'msg':'Product Added'})
    return render(request,'add-product.html',{'uid':uid})

def seller_product(request):
    uid = User.objects.get(email=request.session['email'])
    products = Product.objects.filter(uid=uid)
    # print(products)
    return render(request,'seller-product.html',{'uid':uid,'products':products})

def edit_product(request,pk):
    product = Product.objects.get(id=pk)
    
    uid = User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        product.name = request.POST['name']
        product.des = request.POST['des']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        product.category = request.POST['category']
        if 'pic' in request.FILES:
            product.pic = request.FILES['pic']
            
        product.save()
        return redirect('seller-product')

    return render(request,'edit-product.html',{'uid':uid,'product':product})

def delete_product(request,pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('seller-product')

def all_product(request):
    uid = User.objects.get(email=request.session['email'])
    products = Product.objects.all().order_by('?')

    return render(request,'all-product.html',{'uid':uid,'products':products})

def view_product(request,pk):
    product = Product.objects.get(id=pk)
    uid = User.objects.get(email=request.session['email'])
    cate = product.category
    many = Product.objects.filter(category=product.category)
    # print(many)
    return render(request,'single-product.html',{"uid":uid,'product':product,'many':many})


def add_to_cart(request,pk):
    uid = User.objects.get(email= request.session['email'])
    product = Product.objects.get(id=pk)
    many = Product.objects.filter(category=product.category)

    try:
        cart = Cart.objects.get(uid=uid)
    except:
        Cart.objects.create(uid=uid)
        cart = Cart.objects.get(uid=uid)

    cart.product.add(product)
    return render(request,'single-product.html',{"uid":uid,'product':product,'many':many})

def view_cart(request):
    uid = User.objects.get(email=request.session['email'])
    try:
        cart = Cart.objects.get(uid=uid)
        return render(request,'view-cart.html',{'uid':uid,'cart':cart})
    except:
        return render(request,'view-cart.html',{'uid':uid})

def delete_cart(request,pk):
    uid = User.objects.get(email=request.session['email'])
    product = Product.objects.get(id=pk)
    cart = Cart.objects.get(uid=uid)
    cart.product.remove(product)
    print(cart.product.all().count())
    return redirect('view-cart')

# def buy_product(request,pk):
#     if request.method == 'POST':
#         uid = User.objects.get(email=request.session['email'])
#         product = Product.objects.get(id=pk)
#         quantity = request.POST['quantity']
#         return render(request,'order-confirm.html',{'uid':uid,'product':product,'quantity':quantity})

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 
def buy_product(request,pk):
    global temp
    global address

    uid = User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        quantity = request.POST['quantity'] 
        try:
            address = request.POST['address']
        except:
            address =  'uid.address'
    address = uid.address if 'address' not in request.POST else request.POST['address']
    
    temp = {
        'uid' : uid,
        'product' : product,
        'quantity' : quantity,
        'address' : address
    }
    print(address)
    currency = 'INR'
    amount =  (int(product.price)*int(quantity))*100  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['uid'] = uid
    context['product'] = product
    # context['quantity'] = quantity
 
    return render(request, 'order-confirm.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                global temp, address

                amount = int(temp['product'].price)*int(temp['quantity'])*100  # Rs. 200
                try:
                    today = date.today()
                    if today.day > 23:
                        day = '0'+str(randrange(3,5))
                        if today.month == 12:
                            month = 1
                            year = today.year + 1
                        else:
                            month = today.month + 1
                            year = today.year
                    else:
                        day = today.day + 7
                        month = today.month
                        year = today.year
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    Buy.objects.create(
                        uid = temp['uid'],
                        product = temp['product'],
                        quantity = temp['quantity'],
                        pay_amount = amount/100,
                        pay_id = payment_id,
                        order_id = 'fdgdfgdf',
                        address = temp['address'],
                        expected_del = f'{year}-{month}-{day}',
                    )
                    temp['product'].quantity -= temp['quanntity']
                    temp['product'].save()
                    try:
                        del temp
                    except:
                        pass
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
                    try:
                        del temp
                    except:
                        pass
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
                try:
                    del temp
                except:
                    pass
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
            try:
                del temp
            except:
                pass
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        try:
            del temp
        except:
            pass
       # if other than POST request is made.
        return HttpResponseBadRequest()

def seller_buy_product(request):
    uid = User.objects.get(email=request.session['email'])
    buys = Buy.objects.all()
    select = False
    if request.method == 'POST':
        select = request.POST['search']
        if select == 'pending':
            select = False
        else:
            select = True
    return render(request,'seller-buy-product.html',{'uid':uid,'buys':buys,'select':select})

def view_buy_product(request,pk):
    uid = User.objects.get(email=request.session['email'])
    buy = Buy.objects.get(id=pk)
    return render(request,'view-buy-product.html',{'buy':buy,'uid':uid})

def complete_del(request,pk):
    buy = Buy.objects.get(id=pk)
    buy.status = True
    buy.save()

    return redirect('seller-buy-product')