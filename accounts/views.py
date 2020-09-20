from django.shortcuts import render
from .models import Profile
from .forms import (LoginForm ,
                    UserRegistrationForm ,
                    ProfileUpdateForm ,
                    UserUpdateForm ,
                    )
from django.contrib.auth import authenticate ,logout ,login
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from store.models import Product,OrderItem , FullOrder , Purchased_item , ProductCategories


# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('store'))


    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)

            if user:

                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('store'))
                else:
                    return HttpResponse('User is not Active')
            else:
                return HttpResponse('User Not Available')
    else:
        form = LoginForm()

    product_categories = ProductCategories.objects.all()

    context = {
        'product_categories': product_categories,
        'total_item_cart' : 0,
        'form' : form
    }

    return render(request ,'accounts/login.html' ,context )



@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('store'))



def register(request):

    if request.user.is_authenticated:
        return HttpResponse('First logout')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user = user)
            return HttpResponseRedirect(reverse('user_login'))
    else:
        form = UserRegistrationForm()

    product_categories = ProductCategories.objects.all()

    context = {
        'product_categories': product_categories,
        'total_item_cart' : 0,
        'form' : form
    }

    return render(request , 'accounts/register.html',context)



def edit_profile(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))

    total_item_cart = 0

    items = OrderItem.objects.filter(user=request.user)
    for item in items:
        total_item_cart += item.quantity

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST , instance=request.user )
        profile_form = ProfileUpdateForm(request.POST ,
                            instance=request.user.profile,files =request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

        return HttpResponseRedirect(reverse('store'))

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    product_categories = ProductCategories.objects.all()

    context = {
        'product_categories': product_categories,
        'user_form' : user_form,
        'profile_form' : profile_form,
        'total_item_cart' : total_item_cart,
    }

    return render(request,'accounts/edit_profile.html',context)



def profilepage(request,username):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))

    total_item_cart = 0
    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity

    user = User.objects.get(username=username)
    profile = Profile.objects.all()
    orders = FullOrder.objects.filter(user=request.user).order_by('-date_ordered')

    ordered = []
    for order in orders:
        tt = []
        items = Purchased_item.objects.filter(order = order)
        for item in items:
            tt.append(item)
        ordered.append({'order':order , 'items':tt})

    product_categories = ProductCategories.objects.all()

    context = {
        'product_categories': product_categories,
        'ordered' : ordered,
        'profile' : profile,
        'user' : user,
        'total_item_cart' : total_item_cart,
    }


    return render(request,'accounts/profilepage.html',context)