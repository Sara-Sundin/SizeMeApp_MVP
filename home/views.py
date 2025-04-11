from django.shortcuts import render

def home_view(request):
    """
    Display the Home page.
    """
    show_account_deleted_modal = request.session.pop("show_account_deleted_modal", False)
    return render(request, 'home/index.html', {
        "show_account_deleted_modal": show_account_deleted_modal
    })

def starter_plan(request):
    """
    Display the Starter Plan page.
    """
    return render(request, "home/starter_plan.html")


