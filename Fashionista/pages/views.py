from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from . import models

def index(request: HttpRequest) -> HttpResponse:
    context = {
        'listings_count': models.Listing.objects.count(),
        'wardrobes_count': models.Wardrobe.objects.count(),
        'users_count': models.get_user_model().objects.count(),
    }
    return render(request, 'listings/index.html', context)

def rental_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'listings/rental_list.html', {
        'rental_list': models.Listing.objects.all()
    })

def listing_details(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'listings/details.html', {
        'listing': get_object_or_404(models.Listing, pk=pk)
    })

def listing_available(request: HttpRequest, pk:int) -> HttpResponse:
    listing = get_object_or_404(models.Listing, pk=pk)
    listing.is_available = not listing.is_available
    listing.save()
    messages.success(request, f"Listing {listing.name} marked as {'done' if listing.is_available else 'undone'}")
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect(rental_list)

