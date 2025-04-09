from django.shortcuts import render

def home(request):
    """
    Display the Home page.
    """
    return render(request, "home/index.html")

