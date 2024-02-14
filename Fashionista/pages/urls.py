from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='index'),
    path('listings/', views.rental_list, name='rental_list'),
    path('listing/<int:pk>/', views.listing_details, name='listing_details'),
    path('listing/<int:pk>/done/', views.listing_available, name='is_available'),
]