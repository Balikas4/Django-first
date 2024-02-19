from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from . import models
from django.utils.translation import gettext_lazy as _

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
    messages.success(request, "{} {} {} {}".format(
        _('listing').capitalize(),
          listing.name,
        _('marked as'),
        _('available') if listing.is_available else _('unavailable'),
    ))
    return redirect(rental_list)

def wardrobe_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'wardrobes/wardrobe_list.html', {
        'wardrobe_list': models.Wardrobe.objects.all()
    })

def wardrobe_details(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'wardrobes/details.html', {
        'wardrobe': get_object_or_404(models.Wardrobe, pk=pk)
    })

def wardrobe_for_sale(request: HttpRequest, pk:int) -> HttpResponse:
    wardrobe = get_object_or_404(models.Wardrobe, pk=pk)
    wardrobe.is_for_sale = not wardrobe.is_for_sale
    wardrobe.save()
    messages.success(request, "{} {} {} {}".format(
        _('wardrobe').capitalize(),
          wardrobe.name,
        _('marked as'),
        _('for sale') if wardrobe.is_for_sale else _('not for sale'),
    ))
    return redirect(wardrobe_list)

def main_page(request):
    # Add any logic you want for the main page view
    return render(request, 'main_page.html')  # Assuming you have a main_page.html template
