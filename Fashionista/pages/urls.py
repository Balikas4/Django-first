from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dashboard/', views.index, name='index'),
    path('listings/', views.rental_list, name='rental_list'),
    path('listing/<int:pk>/', views.listing_details, name='listing_details'),
    path('listing/<int:pk>/done/', views.listing_available, name='is_available'),
    path('wardrobes/', views.wardrobe_list, name='wardrobe_list'),
    path('wardrobe/<int:pk>/', views.wardrobe_details, name='wardrobe_details'),
    path('wardrobe/<int:pk>/available/', views.wardrobe_for_sale, name='is_for_sale'),
]

urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
