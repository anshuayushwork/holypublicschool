from django.urls import path
from . import views

urlpatterns = [
    # When a user visits '/faculty/', this will call the staff_list_view.
    # The name 'staff-list' allows us to easily refer to this URL in templates.
    path('', views.staff_list_view, name='staff-list'),
]
