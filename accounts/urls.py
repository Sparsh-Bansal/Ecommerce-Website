from django.urls import path
from . import views




urlpatterns = [
    path('login/',views.user_login,name = 'user_login'),
    path('logout/',views.user_logout ,name = 'user_logout'),
    path('register/',views.register,name = 'register'),
    path('edit_profile/',views.edit_profile , name = 'edit_profile'),
    path('profilepage/<str:username>/',views.profilepage,name='profilepage'),
]



