from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

class User(models.Model):

    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    role = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    pic = models.FileField(upload_to='Profile',default='avtar.png')

    def __str__(self):
        return self.email + ' '  + self.fname 

class Contact(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):

    uid = models.ForeignKey(User,on_delete=models.CASCADE)  # seller
    name = models.CharField(max_length=80)
    des = models.TextField(null=True,blank=True)
    price = models.CharField(max_length=10)
    quantity = models.IntegerField()
    category = models.CharField(max_length=20)
    pic = models.FileField(upload_to='Products',null=True,blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):

    uid = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product,related_name='Cart_product')

    def __str__(self):
        return self.uid.fname

class Buy(models.Model):

    uid = models.ForeignKey(User,on_delete=models.CASCADE)  # buyer
    product = models.ForeignKey(Product,on_delete=models.CASCADE)  # product # seller
    quantity = models.IntegerField(default=1)
    pay_amount = models.IntegerField()
    pay_id = models.CharField(max_length=20)
    order_id = models.CharField(max_length=20)
    address = models.TextField(blank=True,null=True)
    coupon = models.CharField(null=True,blank=True,max_length=20)
    order_date = models.DateTimeField(auto_now_add=True)
    expected_del = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.uid.email + ' || ' +  self.product.name



