from django.urls import path
from . import views

urlpatterns = [
    # URL for the list of all albums, e.g., /gallery/
    path('', views.album_list_view, name='album-list'),
    
    # URL for a single album's photos, e.g., /gallery/a1b2c3d4-e5f6.../
    path('<uuid:uid>/', views.album_detail_view, name='album-detail'),
]
