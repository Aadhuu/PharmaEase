from django.contrib import admin

from shop.models import Category, Product

from shop.models import SubCategory

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(SubCategory)