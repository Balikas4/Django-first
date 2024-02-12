from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RentalListingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rental_listings'

    class Meta:
        verbose_name = _('rental_listings')
