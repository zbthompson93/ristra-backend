from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from restaurants import views

urlpatterns = [
    path('restaurants/', views.restaurant_list),
    path('restaurants/<int:pk>/', views.restaurant_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)