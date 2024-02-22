from django import forms
from django.contrib.auth.decorators import login_required
from . import models

class ListingForm(forms.ModelForm):
    class Meta:
        model = models.Listing
        fields = ('name', 'wardrobe', 'description', 'price', 'is_available')