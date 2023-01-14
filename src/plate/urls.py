from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_plate),
    path('get/', views.get_plate),
    path('get/<uuid:pk>/', views.get_plate),
    path('add/', views.AddPlate.as_view())
]
