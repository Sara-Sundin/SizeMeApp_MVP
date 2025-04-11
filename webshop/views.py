from django.shortcuts import render

def webshop_view(request):
    return render(request, 'webshop/webshop.html')
