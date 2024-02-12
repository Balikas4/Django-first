from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

# Model
class Pages(models.Model):
    name = models.CharField(_("name"), max_length=50)
    owner = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("page"), 
        on_delete=models.CASCADE,
        related_name = 'pages',
)
    class Meta:
        verbose_name = _("page")
        verbose_name_plural = _("pages")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("page_detail", kwargs={"pk": self.pk})

# Model
class Wardrobe(models.Model):
    name = models.CharField(_("name"), max_length=50)
    owner = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("wardrobe"), 
        on_delete=models.CASCADE,
        related_name = 'wardrobe'
        )
    
    class Meta:
        verbose_name = _("wardrobe")
        verbose_name_plural = _("wardrobes")
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("wardrobe_detail", kwargs={"pk": self.pk})

# Model 
class Listing(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index = True)
    description = models.TextField(_("description"), blank=True, max_length = 100000)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    wardrobe = models.ForeignKey(
        Wardrobe, 
        verbose_name=_("project"), 
        on_delete=models.CASCADE,
        related_name = 'listing',
        )
    owner = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("owner"), 
        on_delete=models.CASCADE,
        related_name = 'listing',
        )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index = True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index = True)
    is_available = models.BooleanField(_("is available"), db_index = True, default = False)

    class Meta:
        verbose_name = _("listing")
        verbose_name_plural = _("listings")
        ordering = ['is_available', 'created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("listing_detail", kwargs={"pk": self.pk})
