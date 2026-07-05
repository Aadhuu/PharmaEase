from django.shortcuts import render, redirect
from django.views import View

from shop.models import Category, SubCategory,Product

from shop.forms import CategoryForm, ProductForm

from shop.forms import SubCategoryForm


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


class Products(View):
    def get(self, request, i):
        s=SubCategory.objects.get(id=i)
        p=Product.objects.filter(sub_category=s)
        context={'subcategory':s,'products':p}
        return render(request, 'product.html', context)

class ProductDetail(View):
    def get(self, request, i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request, 'productdetail.html', context)

class AddCategory(View):
    def get(self, request):
        form_instance=CategoryForm()
        context={'form':form_instance}
        return render(request, 'addcategory.html', context)
    def post(self, request):
        form_instance=CategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('home')

class AddSubCategory(View):
    def get(self, request):
        form_instance=SubCategoryForm()
        context={'form':form_instance}
        return render(request, 'addsubcategory.html', context)
    def post(self, request):
        form_instance=SubCategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            if form_instance.is_valid():
                form_instance.save()
                return redirect('home')


class AddProduct(View):
    def get(self, request):
        form_instance=ProductForm()
        context={'form':form_instance}
        return render(request, 'addproduct.html', context)
    def post(self, request):
        form_instance=ProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('home')