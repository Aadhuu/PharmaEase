from django.shortcuts import render
from django.views import View

from shop.models import Category, SubCategory,Product


class Home(View):
    def get(self, request):
        c=Category.objects.all()
        context={'categories':c}
        return render(request, 'home.html', context)

class Sub_category(View):
    def get(self, request, i):
        c = Category.objects.get(id=i)
        s=SubCategory.objects.filter(category=c)
        context={'category':c,'subcategory':s}
        return render(request, 'subcategory.html', context)



