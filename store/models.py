from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class ProductCategories(models.Model):

    name = models.CharField(max_length=100,blank=False,null=True)
    image = models.ImageField(null=True,blank=False)

    @property
    def get_imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name



class Product(models.Model):

    category = models.ManyToManyField(ProductCategories)
    name = models.CharField(max_length=100,blank=False,name=False)
    price = models.FloatField(blank=False,null=False)
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



class FullOrder(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    recepient_fullname = models.CharField(max_length=100, null=True, blank=False)
    phone_no = models.IntegerField(null=True, blank=False)
    address_line1 = models.CharField(max_length=200, null=True, blank=False)
    address_line2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=200, null=True,blank=False)
    state = models.CharField(max_length=200, null=True,blank=False)
    country = models.CharField(max_length=100, null=True, blank=False)
    zipcode = models.CharField(max_length=200, null=True,blank=False)
    amount = models.IntegerField(null=True,blank=True)
    transaction_id = models.CharField(max_length=100,null=True,blank=False)
    date_ordered = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return '{}-{}'.format(self.recepient_fullname,self.id)



class Purchased_item(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(FullOrder,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    name = models.CharField(max_length=100, blank=False, name=False)
    price = models.FloatField(blank=False, null=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    @property
    def get_imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def get_total(self):
        total = self.price * self.quantity
        return total

    def __str_ (self):
        return self.name