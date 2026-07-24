import uuid
import razorpay

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from shop.models import Product

from .models import Cart, Order, OrderItem
from .forms import CheckoutForm

from prescriptions.models import Prescription



@method_decorator(login_required, name='dispatch')
class AddtoCart(View):

    def get(self, request, i):

        product = Product.objects.get(id=i)

        cart, created = Cart.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:
            cart.quantity += 1
            cart.save()

        return redirect('cart:cartview')



@method_decorator(login_required, name='dispatch')
class CartView(View):

    def get(self, request):

        cart = Cart.objects.filter(
            user=request.user
        )

        total = sum(
            i.subtotal() for i in cart
        )

        return render(
            request,
            'cart.html',
            {
                'cart':cart,
                'total':total
            }
        )



@method_decorator(login_required, name='dispatch')
class CartDecrement(View):

    def get(self,request,i):

        c=Cart.objects.get(id=i)

        if c.quantity > 1:
            c.quantity -= 1
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



@method_decorator(login_required, name='dispatch')
class Checkout(View):
    def get(self,request):
        form = CheckoutForm()
        cart = Cart.objects.filter(user=request.user)
        prescription_products=[]
        total=sum(i.subtotal() for i in cart)
        for item in cart:
            if item.product.prescription:
                prescription = Prescription.objects.filter(user=request.user, product=item.product).last()
                prescription_products.append(
                    {'product':item.product,'prescription':prescription })
        return render( request,'checkout.html',
                       { 'form':form,'cart_items':cart,'prescription_products':prescription_products,'total':total})



    def post(self,request):
        form = CheckoutForm( request.POST)
        if form.is_valid():
            cart = Cart.objects.filter( user=request.user)
            # Check prescription approval
            # Check prescription upload and approval

            for item in cart:

                if item.product.prescription:

                    uploaded = Prescription.objects.filter(
                        user=request.user,
                        product=item.product
                    ).exists()

                    if not uploaded:
                        messages.warning(
                            request,
                            f"Please upload prescription for {item.product.name}"
                        )

                        return redirect(
                            'cart:checkout'
                        )

                    approved = Prescription.objects.filter(
                        user=request.user,
                        product=item.product,
                        status="Approved"
                    ).exists()

                    if not approved:
                        messages.warning(
                            request,
                            f"{item.product.name} prescription approval pending."
                        )

                        return redirect(
                            'cart:checkout'
                        )
            order=form.save(commit=False)
            order.user=request.user
            total=sum(i.subtotal() for i in cart)
            order.amount=total
            order.save()
            # Online payment

            if order.payment_method=="Online":
                client=razorpay.Client(auth=('rzp_test_T6IP07TeCheda2','S9k2VRBBxxkWL6m0rCxWVd5p'  ))
                response_payment=client.order.create(
                    {
                    'amount':total*100,
                    'currency':'INR'})


                order.order_id=response_payment['id']

                order.save()


                return render(
                    request,
                    'payment.html',
                    {
                    'payment':response_payment
                    }
                )


            # COD

            order.order_id='ord_cod'+uuid.uuid4().hex[:10]

            order.is_ordered=True

            order.billing_completed=True

            order.save()



            for item in cart:

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )


                item.product.stock -= item.quantity

                item.product.save()


            cart.delete()


            return render(
                request,
                'payment.html'
            )

@method_decorator(login_required,name='dispatch')
@method_decorator(csrf_exempt,name='dispatch')
class Paymentsuccess(View):
    def post(self,request):
        print(request.POST)
        id=request.POST.get('razorpay_order_id')
        o=Order.objects.get(order_id=id)
        o.is_ordered = True
        o.billing_completed = True
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