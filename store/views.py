from django.shortcuts import render
from .models import Product , OrderItem
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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

    items = []
    total_cost_cart = 0
    total_item_cart = 0

    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity

        for item in items:
            total_cost_cart += item.get_total

    context = {
        'items': items,
        'total_item_cart': total_item_cart,
        'total_cost_cart': total_cost_cart
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