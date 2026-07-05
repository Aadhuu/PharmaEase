from django import forms

from shop.models import Category, Product, SubCategory


class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields= '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields= ['name', 'description', 'image','price','stock' ,'category','sub_category','prescription']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model=SubCategory
        fields = '__all__'

class StockForm(forms.ModelForm):
    class Meta:
        model=Product
        fields = ['stock']
