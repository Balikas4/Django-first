from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from . import models

def index(request: HttpRequest) -> HttpResponse:
    context = {
        'listings_count': models.Listing.objects.count(),
        'wardrobes_count': models.Wardrobe.objects.count(),
        'users_count': models.get_user_model().objects.count(),
    }
    return render(request, 'listings/index.html', context)

