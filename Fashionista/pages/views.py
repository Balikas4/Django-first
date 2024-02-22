from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from . import models , forms


class WardrobeListView(generic.ListView):
    model = models.Wardrobe
    template_name = 'wardrobes/wardrobe_list.html'
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        if self.request.GET.get('owner'):
            queryset = queryset.filter(owner__username=self.request.GET.get('owner'))
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_list'] = get_user_model().objects.all()
        return context

class WardrobeDetailView(generic.DetailView):
    model = models.Wardrobe
    template_name = 'wardrobes/wardrobe_details.html'
    
    @staticmethod
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
        return redirect('wardrobe_list')


class WardrobeUpdateView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        generic.UpdateView
    ):
    model = models.Wardrobe
    template_name = 'wardrobes/wardrobe_update.html'
    fields = ('name', 'is_for_sale')

    def get_success_url(self) -> str:
        messages.success(self.request, _('wardrobe updated successfully').capitalize())
        return reverse('wardrobe_list')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user


class WardrobeCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Wardrobe
    template_name = 'wardrobes/wardrobe_create.html'
    fields = ('name', 'is_for_sale')

    def get_success_url(self) -> str:
        messages.success(self.request, _('wardrobe created successfully').capitalize())
        return reverse('wardrobe_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class WardrobeDeleteView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        generic.DeleteView
    ):
    model = models.Wardrobe
    template_name = 'wardrobes/wardrobe_delete.html'

    def get_success_url(self) -> str:
        messages.success(self.request, _('wardrobe deleted successfully').capitalize())
        return reverse('wardrobe_list')

    def test_func(self) -> bool | None:
        return self.get_object().owner == self.request.user


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'listings_count': models.Listing.objects.count(),
        'wardrobes_count': models.Wardrobe.objects.count(),
        'users_count': models.get_user_model().objects.count(),
    }
    return render(request, 'listings/index.html', context)

# def rental_list(request: HttpRequest) -> HttpResponse:
#     return render(request, 'listings/rental_list.html', {
#         'rental_list': models.Listing.objects.all()
#     })

def rental_list(request: HttpRequest) -> HttpResponse:
    queryset = models.Listing.objects
    owner_username = request.GET.get('owner')
    if owner_username:
        owner = get_object_or_404(get_user_model(), username=owner_username)
        queryset = queryset.filter(owner=owner)
        wardrobes = models.Wardrobe.objects.filter(owner=owner)
    elif request.user.is_authenticated:
        wardrobes = models.Wardrobe.objects.filter(owner=request.user)
    else:
        wardrobes = models.Wardrobe.objects
    wardrobe_pk = request.GET.get('wardrobe_pk')
    if wardrobe_pk:
        wardrobe = get_object_or_404(models.Wardrobe, pk=wardrobe_pk)
        queryset = queryset.filter(wardrobe=wardrobe)
    search_name = request.GET.get('search_name')
    if search_name:
        queryset = queryset.filter(name__icontains=search_name)
    next = request.path + '?' + '&'.join([f"{key}={value}" for key, value in request.GET.items()])
    context = {
        'rental_list': queryset.all(),
        'wardrobe_list': wardrobes.all(),
        'user_list': get_user_model().objects.all().order_by('username'),
        'next': next,
    }
    return render(request, 'listings/rental_list.html', context)

def listing_available(request: HttpRequest, pk:int) -> HttpResponse:
    listing = get_object_or_404(models.Listing, pk=pk)
    if request.user in [listing.owner, listing.wardrobe.owner]:
        listing.is_available = not listing.is_available
        listing.save()
        messages.success(request, "{} {} {} {}".format(
            _('listing').capitalize(),
            listing.name,
            _('marked as'),
            _('available') if listing.is_available else _('unavailable'),
        ))
    else:
        messages.error(request, "{}: {}".format(_("permission error").title(), _("you must be the owner of either the listing and the wardrobe"),))
    if request.GET.get("next"):
        return redirect(request.GET.get("next"))
    return redirect(rental_list)

def listing_details(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'listings/listing_details.html', {
        'listing': get_object_or_404(models.Listing, pk=pk)
    })

def main_page(request):
    return render(request, 'main_page.html')

@login_required
def listing_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.ListingForm(request.POST)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            messages.success(request, _("listing created successfully").capitalize())
            return redirect('rental_list')
    else:
        form = forms.ListingForm
    return render(request, 'listings/listing_create.html', {'form': form})

@login_required
def listing_update(request: HttpRequest, pk: int) -> HttpResponse:
    listing = get_object_or_404(models.Listing, pk=pk, owner=request.user)
    if request.method == "POST":
        form = forms.ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, _("listings edited successfully"))
            return redirect('listing_details', pk=pk)
    else:
        form = forms.ListingForm(instance=listing)
    form.fields['wardrobe'].queryset = form.fields['wardrobe'].queryset.filter(owner=request.user)
    return render(request, 'listings/listing_update.html', {'form': form})

@login_required
def listing_delete(request: HttpRequest, pk: int) -> HttpResponse:
    listing = get_object_or_404(models.Listing, pk=pk, owner=request.user)
    if request.method == "POST":
        listing.delete()
        messages.success(request, _("listing deleted successfully"))
        return redirect('rental_list')
    return render(request, 'listings/listing_delete.html', {'listing': listing})