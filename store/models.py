from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):

    name = models.CharField(max_length=100,blank=False,name=False)
    price = models.FloatField(blank=False,null=False)
    digital = models.BooleanField(default=False,blank=True,null=True)
    image = models.ImageField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

    @property
    def get_imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



class OrderItem(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0,blank=True,null=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return '{}-{}'.format(self.user.username,self.product.name)



class ShippingAddress(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=False)
    recepient_fullname = models.CharField(max_length=100,null=True,blank=False)
    phone_no = models.IntegerField(null=False,blank=False)
    address_line1 = models.CharField(max_length=200, null=True,blank=False)
    address_line2 = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=100,null=True,blank=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.address_line1, self.address_line2)



class Purchased_item(models.Model):

    address = models.ForeignKey(ShippingAddress,on_delete=models.DO_NOTHING,null=True,blank=False)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True, blank=False)
    amount = models.IntegerField(null=True,blank=False)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100)


    def __str_ (self):
        return '{}-{}'.format(self.user.username,self.product.name)



class FullOrder(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
