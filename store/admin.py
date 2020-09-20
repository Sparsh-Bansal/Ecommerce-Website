from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Product)
admin.site.register(models.OrderItem)
admin.site.register(models.ShippingAddress)
admin.site.register(models.Purchased_item)
admin.site.register(models.FullOrder)
admin.site.register(models.ProductCategories)
