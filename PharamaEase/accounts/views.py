from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import RegisterForm


class Register(View):
    def post(self,request):
        form_instance = RegisterForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('accounts:userlogin')

    def get(self,request):
        form_instance = RegisterForm()
        context = {'form':form_instance}
        return render(request,'register.html',context)