from django.urls import path
from . import views

urlpatterns = [
    # Map the root URL ('') to our home_view
    path('', views.home_view, name='home'),
    path('contact/', views.contact_view, name='contact'),
    
]
