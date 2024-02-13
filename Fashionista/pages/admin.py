from django.contrib import admin
from . import models
from django.utils.translation import gettext_lazy as _


class WardrobeAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'total_listings', 'available_listings', 'recent_listings']
    list_display_links = ['name', 'owner']
    list_filter = ['owner']
    search_fields = ['name', 'owner']
    readonly_fields = ['total_listings']
    fieldsets = (
        (None, {
            "fields": (
                'name', 'owner', 'total_listings',
            ),
        }),
    )

    def total_listings(self, obj):
        return obj.listings.count()
    
    total_listings.short_description = _("total listings")

    def available_listings(self, obj):
        return obj.listings.filter(is_available=True).count()

    available_listings.short_description = _("available listings")

    def recent_listings(self, obj):
        return "; ".join(obj.listings.order_by('-created_at').values_list('name', flat=True)[:3])
    
    recent_listings.short_description = _("recent listings")


class ListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'description', 'is_available', 'created_at', 'updated_at', 'owner', 'wardrobe']
    list_filter = ['is_available', 'created_at', 'is_available', 'wardrobe']
    search_fields = ['name', 'description', 'listing__name', 'owner__last_name', 'wardrobe__name']
    list_editable = ['is_available']
    list_display_links = ['owner', 'wardrobe']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        (_("general").title(), {
            "fields": (
                ('name', 'price', 'wardrobe'),
                'description', 'is_available',
            ),
        }),
        (_("ownership").title(), {
            "fields": (
                ('owner', 'id'),
            ),
        }),
        (_("temporal tracking").title(), {
            "fields": (
                ('created_at', 'updated_at'),
            ),
        }),
    )


admin.site.register(models.Wardrobe, WardrobeAdmin)
admin.site.register(models.Listing, ListingAdmin)
