from django.shortcuts import render


def index(request):
    """Render Simple Page"""
    context = {}
    return render(request, 'main/index.html', context)
