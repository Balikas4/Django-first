from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('dashboard/', views.index, name='index'),
    path('listings/', views.rental_list, name='rental_list'),
    path('listing/<int:pk>/', views.listing_details, name='listing_details'),
    path('listing/<int:pk>/done/', views.listing_available, name='is_available'),
    path('wardrobe/<int:pk>/available/', views.WardrobeDetailView.wardrobe_for_sale, name='is_for_sale'),
    path('wardrobes/', views.WardrobeListView.as_view(), name='wardrobe_list'),
    path('wardrobe/<int:pk>/', views.WardrobeDetailView.as_view(), name='wardrobe_detail'),
    path('wardrobe/create/', views.WardrobeCreateView.as_view(), name='wardrobe_create'),
    path('wardrobe/<int:pk>/edit/', views.WardrobeUpdateView.as_view(), name='wardrobe_update'),
    path('wardrobe/<int:pk>/delete/', views.WardrobeDeleteView.as_view(), name='wardrobe_delete'),
]

urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
