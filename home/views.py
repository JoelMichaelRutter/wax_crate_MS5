from django.shortcuts import render


def index(request):
    """
    Renders the index page in the home app.
    """
    return render(request, 'home/index.html')
