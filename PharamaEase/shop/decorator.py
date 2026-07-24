from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages


def admin_required(fun):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser == False:
            messages.error(request, "You are not authorized to view this page.")
            return render(request,'error.html')
        else:
            return fun(request, *args, **kwargs)

    return wrapper
