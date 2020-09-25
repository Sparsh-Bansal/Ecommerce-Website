from store.models import Product , OrderItem , ShippingAddress , FullOrder , Purchased_item
from store.models import ProductCategories
from django.http import JsonResponse
from .serializers import(
    ProductCategorySerializer,
    OrderItemSerializer,
    ProductSerializer,
    OrderDetailsSerializer,
    ShippingAddressSerializer,
)
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers

# Create your views here.



class Store(APIView):

    def get(self,request):

        total_item_cart = 0

        if request.user.is_authenticated:
            items = OrderItem.objects.filter(user=request.user)
            for item in items:
                total_item_cart += item.quantity


        product_categories = ProductCategories.objects.all()
        serializer_pct = ProductCategorySerializer(product_categories,many=True)
        context = {
            'product_categories' : serializer_pct.data,
            'total_item_cart' : total_item_cart,
        }

        return Response(context)



class Cart(APIView):

    def get(self,request):

        items = []
        total_cost_cart = 0
        total_item_cart = 0

        if request.user.is_authenticated:
            items = OrderItem.objects.filter(user=request.user)
            for item in items:
                total_item_cart += item.quantity

            for item in items:
                total_cost_cart += item.get_total

        product_categories = ProductCategories.objects.all()
        serializer_pct = ProductCategorySerializer(product_categories,many=True)
        serializer_OI = OrderItemSerializer(items,many=True)
        context = {
            'items': serializer_OI.data,
            'total_item_cart': total_item_cart,
            'total_cost_cart': total_cost_cart,
            'product_categories': serializer_pct.data,
        }
        return Response(context)



class Checkout(APIView):

    def get(self,request):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        items = []
        total_cost_cart = 0
        total_item_cart = 0

        if request.user.is_authenticated:
            items = OrderItem.objects.filter(user=request.user)
            for item in items:
                total_item_cart += item.quantity

            for item in items:
                total_cost_cart += item.get_total

        if total_item_cart == 0:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer_OI = OrderItemSerializer(items, many=True)

        product_categories = ProductCategories.objects.all()
        serializer_pct = ProductCategorySerializer(product_categories, many=True)

        addresses = ShippingAddress.objects.filter(user = request.user)
        serializer_adr = ShippingAddressSerializer(addresses,many=True)

        context = {
            'product_categories' : serializer_pct.data,
            'items': serializer_OI.data,
            'total_item_cart': total_item_cart,
            'total_cost_cart': total_cost_cart,
            'addresses' : serializer_adr.data,
        }
        return Response(context)



class ShowItems(APIView):

    def get(self,request,id):

        total_item_cart = 0

        if request.user.is_authenticated:
            items = OrderItem.objects.filter(user=request.user)
            for item in items:
                total_item_cart += item.quantity
        try:
            product_category = ProductCategories.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer_pct_1 = ProductCategorySerializer(product_category)

        products = Product.objects.filter(category=product_category)
        serializer_P = ProductSerializer(products,many=True)

        product_categories = ProductCategories.objects.all()
        serializer_pct = ProductCategorySerializer(product_categories,many=True)

        context = {
            'product_categories': serializer_pct.data,
            'product_category': serializer_pct_1.data,
            'products': serializer_P.data,
            'total_item_cart': total_item_cart,
        }
        return Response(context)



class ItemDetail(APIView):

    def get(self,request,id):

        total_item_cart = 0

        if request.user.is_authenticated:
            items = OrderItem.objects.filter(user=request.user)
            for item in items:
                total_item_cart += item.quantity
        try:
            product = Product.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer_P = ProductSerializer(product)

        product_categories = ProductCategories.objects.all()
        serializer_pct = ProductCategorySerializer(product_categories,many=True)

        context = {
            'product_categories': serializer_pct.data,
            'product': serializer_P.data,
            'total_item_cart': total_item_cart,
        }

        return Response(context)



class OrderDetails(APIView):

    def get(self,request):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        total_item_cart = 0
        if request.user.is_authenticated:
            items = OrderItem.objects.filter(user=request.user)
            for item in items:
                total_item_cart += item.quantity

        orders = FullOrder.objects.filter(user=request.user).order_by('-date_ordered')

        ordered = []
        for order in orders:
            items = Purchased_item.objects.filter(order=order)
            tt = serializers.serialize('json',items)
            serializer_order = OrderDetailsSerializer(order)
            ordered.append({'order': serializer_order.data, 'items': tt})

        product_categories = ProductCategories.objects.all()
        serializer_pct = ProductCategorySerializer(product_categories,many=True)

        context = {
            'product_categories': serializer_pct.data,
            'ordered': ordered,
            'total_item_cart': total_item_cart,
        }
        return Response(context)



class Search(APIView):

    def post(self,request):

        total_item_cart = 0
        query = request.data['search']

        if request.user.is_authenticated:
            items = OrderItem.objects.filter(user=request.user)
            for item in items:
                total_item_cart += item.quantity

        product_categories = ProductCategories.objects.all()
        serializer_pct = ProductCategorySerializer(product_categories,many=True)

        products_temp = Product.objects.all()

        products = []

        for p in products_temp:
            if query.lower() in p.name.lower() or query.lower() in p.description.lower():
                products.append(p)

        products_json = serializers.serialize('json',products)
        context = {
            'products': products_json,
            'product_categories': serializer_pct.data,
            'total_item_cart': total_item_cart,
        }

        return Response(context)


@method_decorator(csrf_exempt, name='dispatch')
class InsertIntoCart(APIView):

    def post(self,request):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        total_item_cart = 0

        product_id = request.data['product_id']
        action = request.data['action']
        product = Product.objects.get(id=product_id)

        item , created = OrderItem.objects.get_or_create(product=product,user=request.user)
        item.save()
        if action == 'add':
            item.quantity+=1
            item.save()
        else:
            item.quantity-=1
            item.save()
            if item.quantity <=0:
                item.delete()

        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity

        dic = {
            'total_item_cart': total_item_cart,
        }

        return Response(dic)


class Address(APIView):

    def get(self,request):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        addresses = ShippingAddress.objects.filter(user=request.user)
        serializer_adr = ShippingAddressSerializer(addresses,many=True)
        context = {
            'addresses' : serializer_adr.data
        }
        return Response(context)


    def post(self,request):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        request.data["user"] = self.request.user.id
        serializer_adr = ShippingAddressSerializer(data=request.data)

        if serializer_adr.is_valid():
            serializer_adr.save(user=request.user)
            return Response(serializer_adr.data,status=status.HTTP_201_CREATED)
        return Response(serializer_adr.errors,status=status.HTTP_400_BAD_REQUEST)



class AddressDetail(APIView):

    def get(self,request,id):

        try:
            adr = ShippingAddress.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if adr.user != request.user:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        serializer_adr = ShippingAddressSerializer(adr)
        context = {
            'address' : serializer_adr.data
        }
        return Response(context)


    def put(self,request,id):

        try:
            adr = ShippingAddress.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if adr.user != request.user:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        serializer_adr = ShippingAddressSerializer(adr,request.data)
        if serializer_adr.is_valid():
            serializer_adr.save()
            return Response(serializer_adr.data,status=status.HTTP_201_CREATED)
        return Response(serializer_adr.errors,status=status.HTTP_400_BAD_REQUEST)



    def delete(self,request,id):

        adr = ShippingAddress.objects.get(id=id)
        if adr.user != request.user:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        adr.delete()
        return Response(status=status.HTTP_200_OK)


class MakePayment(APIView):

    def get(self,request,id):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

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

        return Response(status=status.HTTP_200_OK)
