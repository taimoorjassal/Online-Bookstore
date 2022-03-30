from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    #user can only have one customer and vice versa, therofore one to one relation
    #if user gets deleted the customer field also gets deleted
    user    = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
    email   = models.CharField(max_length=200, null=True)   
    name    = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name    = models.CharField(max_length=200, null=True)
    author  = models.CharField(max_length=200, null=True)
    price   = models.FloatField()
    digital = models.BooleanField(default = False, null = True, blank = False)
    image   = models.ImageField(null = True, blank = True)
    description = models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''

        return url


class Order(models.Model):
    '''many to one relation as  a customer can have multiple orders
       but one order belongs to only one customer.'''

    '''if the customer gets deleted the value of customer.order is set to null
       instead of deletingt the order'''

    customer        = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
    date_ordered    = models.DateTimeField(auto_now_add=True)#adds current date
    complete        = models.BooleanField(default = False)
    transaction_id  = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

class OrderItem(models.Model):
    product     = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)

    #a single order can have multiple order items
    order       = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    quantity    = models.IntegerField(default = 0, null = True, blank = True)
    date_added  = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Shipping(models.Model):
    customer    = models.ForeignKey(Customer, on_delete=models.SET_NULL, null = True)
    order       = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    address     = models.CharField(max_length=200, null=True)
    city        = models.CharField(max_length=200, null=True)
    state       = models.CharField(max_length=200, null=True)
    zipcode     = models.CharField(max_length=200, null=True)
    date_added  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
