from django import forms
from . import models


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Listing
        fields = ('name', 'wardrobe', 'description', 'is_available')