from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect


## Create your views here.

@login_required()
def home(request):
    return render(request, "index.html")

@login_required()
def logoutUser(request):
    logout(request)
    return redirect('/login/')

