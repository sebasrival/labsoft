from django.shortcuts import render

def home(request):
    return render(request, "vali-admin/dashboard.html")
