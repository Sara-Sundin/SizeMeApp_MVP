from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def webshop_view(request):
    if 'size_mode' not in request.session:
        request.session['size_mode'] = True
    return render(request, 'webshop/webshop.html')


@login_required
def update_measurements_from_webshop(request):
    if request.method == 'POST':
        user = request.user
        user.chest = request.POST.get('chest')
        user.waist = request.POST.get('waist')
        user.hips = request.POST.get('hips')
        user.shoulders = request.POST.get('shoulders')
        user.save()
        request.session['show_measurements_success'] = True
    return redirect(request.META.get('HTTP_REFERER', 'products'))

