import uuid

import razorpay
from django.shortcuts import render, redirect

from django.views import View

from cart.models import Cart
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product

from cart.forms import CheckoutForm

from cart.models import Order

from cart.models import OrderItem
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required,name='dispatch')
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

@method_decorator(login_required,name='dispatch')
class CartView(View):
    def get(self,request):
        c=Cart.objects.filter(user=request.user)
        total=0
        for i in c:
            total+=i.subtotal()
        context={'total':total,'cart':c}
        return render(request,'cart.html',context)

@method_decorator(login_required,name='dispatch')
class CartDecrement(View):
    def get(self,request,i):
        c=Cart.objects.get(id=i)
        if c.quantity>1:
            c.quantity-=1
            c.save()
        else:
            c.delete()
        return redirect('cart:cartview')

@method_decorator(login_required, name='dispatch')
class CartRemove(View):
    def get(self,request,i):
        c=Cart.objects.get(id=i)
        c.delete()
        return redirect('cart:cartview')

@method_decorator(login_required,name='dispatch')
class Checkout(View):
    def post(self,request):
        form_instance=CheckoutForm(request.POST,request.FILES)
        if form_instance.is_valid():
            o=form_instance.save(commit=False)
            u=request.user
            o.user=u
            c=Cart.objects.filter(user=u)
            total=0
            for i in c:
                total+=i.subtotal()
            o.amount=total
            o.save()
            if o.payment_method == "Online":
                client=razorpay.Client(auth=('rzp_test_T6IP07TeCheda2','S9k2VRBBxxkWL6m0rCxWVd5p'))
                print(client)

                response_payment=client.order.create(dict(amount=total*100,currency='INR'))
                print(response_payment)

                o.order_id=response_payment['id']
                o.save()

                context = {'payment': response_payment}
                return render(request, 'payment.html', context)
            else:
                id='ord_cod'+uuid.uuid4().hex[:14]
                o.order_id=id
                o.is_ordered = True
                o.save()
                c = Cart.objects.filter(user=request.user)
                for i in c:
                    item = OrderItem.objects.create(order=o, product=i.product, quantity=i.quantity)
                    item.save()
                    item.product.stock = item.quantity
                    item.product.save()

                c.delete()

                return render(request,'payment.html')
    def get(self,request):
        form_instance=CheckoutForm()
        cart=Cart.objects.filter(user=request.user)
        prescription=False
        for i in cart:
            if i.product.prescription:
                prescription=True
                break
        context={'form':form_instance,'prescription':prescription}
        return render(request,'checkout.html',context)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(login_required,name='dispatch')
@method_decorator(csrf_exempt,name='dispatch')
class Paymentsuccess(View):
    def post(self,request):
        print(request.POST)
        id=request.POST.get('razorpay_order_id')
        o=Order.objects.get(order_id=id)
        o.is_ordered = True
        o.save()
        c=Cart.objects.filter(user=request.user)
        for i in c:
            item=OrderItem.objects.create(order=o,product=i.product,quantity=i.quantity)
            item.save()
            item.product.stock=item.quantity
            item.product.save()

        c.delete()

        return render(request,'paymentsuccess.html')

@method_decorator(login_required,name='dispatch')
class MyOrder(View):
    def get(self,request):
        o=Order.objects.filter(user=request.user)
        context={'orders':o}
        return render(request,'myorder.html',context)