from django.shortcuts import render

def webshop_view(request):
    if 'size_mode' not in request.session:
        request.session['size_mode'] = True
    return render(request, 'webshop/webshop.html')
