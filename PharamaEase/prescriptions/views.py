from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import PrescriptionForm
from shop.models import Product


@method_decorator(login_required, name='dispatch')
class UploadPrescription(View):

    def get(self, request, product_id):

        form = PrescriptionForm()

        product = Product.objects.get(id=product_id)

        return render(
            request,
            'upload_prescription.html',
            {
                'form': form,
                'product': product
            }
        )


    def post(self, request, product_id):

        form = PrescriptionForm(
            request.POST,
            request.FILES
        )

        product = Product.objects.get(id=product_id)


        if form.is_valid():

            prescription = form.save(commit=False)

            prescription.user = request.user
            prescription.product = product
            prescription.status = "Pending"

            prescription.save()


            messages.success(
                request,
                "Prescription uploaded successfully. Please wait for admin approval."
            )


            return redirect(
                'cart:checkout'
            )


        return render(
            request,
            'upload_prescription.html',
            {
                'form': form,
                'product': product
            }
        )