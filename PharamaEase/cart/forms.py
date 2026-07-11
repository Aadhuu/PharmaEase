from django import forms

from PharamaEase.cart.models import Checkout


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields=['full_name','phone','email','address','city','state','pincode','payment_method','prescription']