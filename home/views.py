from django.shortcuts import render

def home(request):
    """
    Display the Home page.
    """
    return render(request, "home/index.html")

def starter_plan(request):
    """
    Display the Starter Plan page.
    """
    return render(request, "home/starter_plan.html")

