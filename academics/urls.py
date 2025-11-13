from django.urls import path
from . import views

urlpatterns = [
    # URL for the main academics page, e.g., /academics/
    path('', views.academic_info_view, name='academic-info'),
]
