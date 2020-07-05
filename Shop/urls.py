from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from django.contrib.auth.decorators import login_required


from . import views

urlpatterns = [
   path('home/', views.home, name="home"),
   path('product/<int:id>/', views.product_detail),
   path('search/', views.search),
   path('brand/<str:name>/', views.brand_detail),
   path('product/post/', views.product_create_view),
   path('product/update/<int:pk>/',
         views.product_update_view, name="updateproduct"),
   path('product/delete/', login_required(views.DeleteProduct.as_view()), name="deleteproduct"),
   path('autocomplete/', views.autocomplete, name="autocomplete"),
   
]

app_name = 'Shop'
