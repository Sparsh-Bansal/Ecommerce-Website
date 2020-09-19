from django.shortcuts import render
from .models import Product , OrderItem , ShippingAddress , FullOrder , Purchased_item
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ShippingForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
import datetime
import json


# Create your views here.
def store(request):

    total_item_cart = 0

    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity

    products = Product.objects.all()

    context = {
        'products' : products,
        'total_item_cart' : total_item_cart,
    }
    return render(request, 'store/store.html', context)



def cart(request):

    items = []
    total_cost_cart=0
    total_item_cart=0

    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user = request.user)
        for item in items:
            total_item_cart += item.quantity

        for item in items:
            total_cost_cart += item.get_total

    context = {'items' : items , 'total_item_cart' : total_item_cart
               ,'total_cost_cart' : total_cost_cart}
    return render(request, 'store/cart.html', context)



def checkout(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))

    items = []
    total_cost_cart = 0
    total_item_cart = 0

    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity

        for item in items:
            total_cost_cart += item.get_total

    form = ShippingForm()
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            adr = form.save(commit=False)
            adr.user = request.user
            adr.save()
        return HttpResponseRedirect(reverse('checkout'))

    addresses = ShippingAddress.objects.filter(user = request.user)

    context = {
        'items': items,
        'total_item_cart': total_item_cart,
        'total_cost_cart': total_cost_cart,
        'form' : form,
        'addresses' : addresses,
    }
    return render(request, 'store/checkout.html', context)



@csrf_exempt
def insert_into_cart(request):

    total_item_cart = 0
    about = 'item_not_added'
    if request.user.is_authenticated:
        about = 'Item Added'
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id = product_id)
        if OrderItem.objects.filter(product=product,user = request.user).exists():
            item = OrderItem.objects.get(product=product,user = request.user)
            item.quantity += 1
            item.save()
        else:
            item = OrderItem.objects.create(product=product,user = request.user,quantity =1)
            item.save()

        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity


    dic = {
        'data' : about,
        'total_item_cart' : total_item_cart,
    }
    return JsonResponse(dic, safe=False)



@csrf_exempt
def update_item_quantity(request):
    about = 'Some Error Occurred'
    if request.user.is_authenticated:
        about = 'Item Updated'
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        product = Product.objects.get(id=product_id)
        item = OrderItem.objects.get(product=product, user=request.user)

        if action == 'add':
            item.quantity+=1
        else:
            item.quantity-=1
        item.save()
        if item.quantity <= 0 :
            item.delete()

    dic = {
        'data': about,
    }
    return JsonResponse(dic,safe=False)



def item_detail(request,id):
    total_item_cart = 0

    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity
    product = Product.objects.get(id=id)
    context = {
        'product' : product,
        'total_item_cart' : total_item_cart,
    }
    return render(request,'store/item_detail.html',context)



def make_payment(request,id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))

    dt = datetime.datetime.now()
    seq = int(dt.strftime("%Y%m%d%H%M%S"))

    adr = ShippingAddress.objects.get(id = id)
    obj = FullOrder.objects.create(user = request.user)

    obj.recepient_fullname = adr.recepient_fullname
    obj.phone_no = adr.phone_no
    obj.address_line1 = adr.address_line1
    obj.address_line2 = adr.address_line2
    obj.city = adr.city
    obj.state = adr.state
    obj.country = adr.country
    obj.zipcode = adr.zipcode
    obj.transaction_id = seq
    obj.save()

    total_amount = 0
    items = OrderItem.objects.all()
    for item in items:
        item_purchased = Purchased_item.objects.create(order = obj)
        item_purchased.user = request.user
        item_purchased.quantity = item.quantity
        item_purchased.name = item.product.name
        item_purchased.price = item.product.price
        item_purchased.image = item.product.image
        item_purchased.description = item.product.description
        item_purchased.save()
        total_amount += item.product.price * item.quantity

        item.delete()

    obj.amount = total_amount
    obj.save()
    context = {
        'total_amount' : total_amount,
    }

    return JsonResponse(context,safe=False)
