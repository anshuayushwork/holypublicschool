from django.urls import path
from . import views

urlpatterns = [
    # URL for the list of all posts, e.g., /blog/
    path('', views.post_list_view, name='post-list'),
    
    # URL for a single post detail, e.g., /blog/a1b2c3d4-e5f6.../
    # It captures the UUID from the URL and passes it to the view.
    path('<uuid:uid>/', views.post_detail_view, name='post-detail'),
]
