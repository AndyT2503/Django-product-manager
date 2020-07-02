from django.conf.urls import include, url
from django.urls import path

from . import views

urlpatterns = [
   url(r'^/?$', views.home),
   url(r'^home/?$', views.home),
   path('product/<int:id>/', views.product_detail),
   path('search/', views.search),
   path('brand/<str:name>/', views.brand_detail),
   path('product/post/', views.product_create_view),
   path('product/update/<int:pk>/', views.product_update_view, name = "updateproduct"),
   path('product/delete/', views.DeleteProduct.as_view(), name = "deleteproduct"),


]

app_name = 'Shop'