from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    def subtotal(self):
        return self.quantity * self.product.price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    order_id = models.CharField(max_length=20, unique=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    payment_method= models.CharField(max_length=100,default="")
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone = models.IntegerField(max_length=50)
    is_ordered = models.BooleanField(default=False)
    delivery_status=models.CharField(max_length=100,default="pending")
    prescription=models.FileField(upload_to='prescriptions',null=True,blank=True)
    order_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.order_id

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.order.order_id