from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dashboard/', views.index, name='index'),
    path('listings/', views.rental_list, name='rental_list'),
    path('listing/<int:pk>/', views.listing_details, name='listing_details'),
    path('listing/<int:pk>/done/', views.listing_available, name='is_available'),
]

urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))