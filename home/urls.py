from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('', views.home),
    path('signup', views.handleSignup),
    path('login', views.handleLogin),
    path('logout', views.handleLogout),
    path('sellbook', views.sellbook),
    path('savebook', views.savebook),
    path('loginsignup',views.loginsignup,name='loginsignup'),
    path('TrackOrder',views.TrackOrder,name='TrackOrder'),
    path('search',views.search,name='search'),
    path('checkout',views.checkout,name='checkout'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
