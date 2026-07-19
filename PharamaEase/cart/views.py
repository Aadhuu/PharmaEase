from http.client import responses

import razorpay
from django.shortcuts import render, redirect
from django.views import View

from cart.models import Cart
from shop.models import Product

from cart.forms import CheckoutForm


class AddtoCart(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        try:
            c=Cart.objects.get(user=u,product=p)
            c.quantity+=1
            c.save()
        except:
            c=Cart.objects.create(user=u,product=p,quantity=1)
            c.save()

        return redirect('cart:cartview')

class CartView(View):
    def get(self,request):
        c=Cart.objects.filter(user=request.user)
        total=0
        for i in c:
            total+=i.subtotal()
        context={'total':total,'cart':c}
        return render(request,'cart.html',context)

class CartDecrement(View):
    def get(self,request,i):
        c=Cart.objects.get(id=i)
        if c.quantity>1:
            c.quantity-=1
            c.save()
        else:
            c.delete()
        return redirect('cart:cartview')
class CartRemove(View):
    def get(self,request,i):
        c=Cart.objects.get(id=i)
        c.delete()
        return redirect('cart:cartview')

class Checkout(View):
    def post(self,request):
        form_instance=CheckoutForm(request.POST,request.FILES)
        if form_instance.is_valid():
            o=form_instance.save(commit=False)
            u=request.user
            o.user=u

            c=Cart.objects.get(user=u)
            total=0
            for i in c:
                total+=i.subtotal()
            o.amount=total
            o.save()
            if o.payment_method == "Online Payment":
                client=razorpay.Client(auth=('rzp_test_T6IP07TeCheda2','S9k2VRBBxxkWL6m0rCxWVd5p'))
                print(client)
            else:
                pass

    def get(self,request):
        form_instance=CheckoutForm()
        c=Cart.objects.filter(user=request.user)
        prescription=False
        for i in c:
            if i.product.prescription:
                prescription=True
                break
        context={'form':form_instance,'prescription':prescription}
        return render(request,'checkout.html',context)



