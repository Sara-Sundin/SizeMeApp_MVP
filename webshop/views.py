from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def webshop_view(request):
    """
    Render the main webshop landing page.

    If 'size_mode' is not already set in the user's session, 
    it will default to True. This is used to enable size-related 
    features in the frontend.
    """
    if 'size_mode' not in request.session:
        request.session['size_mode'] = True
    return render(request, 'webshop/webshop.html')


@login_required
def update_measurements_from_webshop(request):
    """
    Update the authenticated user's body measurements 
    from the webshop modal form.

    This view is called when the user submits their 
    chest, waist, hips, and shoulders from the webshop.
    A success flag is stored in the session to trigger a modal.
    """
    if request.method == 'POST':
        user = request.user
        # Get measurements from POST data
        user.chest = request.POST.get('chest')
        user.waist = request.POST.get('waist')
        user.hips = request.POST.get('hips')
        user.shoulders = request.POST.get('shoulders')
        user.save()

        # Set session flag to show success modal after redirect
        request.session['show_webshop_measurements_success'] = True

    # Redirect back to the referring page, or fallback to 'products' view
    return redirect(request.META.get('HTTP_REFERER', 'products'))
