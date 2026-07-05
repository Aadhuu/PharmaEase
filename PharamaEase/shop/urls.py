"""
URL configuration for PharamaEase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views

app_name='shop'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('subcategory/<int:i>',views.Sub_category.as_view(),name='subcategory'),
    path('product/<int:i>',views.Products.as_view(),name='product'),
    path('productdetail/<int:i>',views.ProductDetail.as_view(),name='productdetail'),
    path('addproduct',views.AddProduct.as_view(),name='addproduct'),
    path('addcategory',views.AddCategory.as_view(),name='addcategory'),
    path('addsubcategory',views.AddSubCategory.as_view(),name='addsubcategory'),
    path('addstock/<int:i>',views.AddStock.as_view(),name='addstock'),

]
