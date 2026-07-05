from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import RegisterForm

from accounts.forms import LoginForm


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

from django.contrib.auth import logout,login,authenticate
from django.contrib import messages

class UserLogin(View):
    def get(self,request):
        form_instance = LoginForm()
        context = {'form':form_instance}
        return render(request,'login.html',context)
    def post(self,request):
        form_instance = LoginForm(request.POST)
        if form_instance.is_valid():
            data = form_instance.cleaned_data
            print(data)
            u=data['username']
            p=data['password']
            user=authenticate(username=u,password=p)

            if user:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'Email or Password is incorrect')
                return redirect('accounts:userlogin')

class UserLogout(View):
    def get(self,request):
        logout(request)
        return redirect('accounts:userlogin')