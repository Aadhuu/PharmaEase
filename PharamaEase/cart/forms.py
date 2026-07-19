from django import forms

from cart.models import Order


class CheckoutForm(forms.ModelForm):
    payment_choices = (('Cash on delivery', 'Cash on delivery'), ('Online', 'Online'))
    payment_method = forms.ChoiceField(choices=payment_choices)
    class Meta:
        model = Order
        fields=['full_name','phone','address','city','state','pincode','payment_method','prescription']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'prescription': forms.ClearableFileInput(attrs={'class': 'form-control'}),}