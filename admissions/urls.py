# admissions/urls.py

from django.urls import path
from . import views
from .views import find_application_view ,admission_procedure_view, fee_structure_view


urlpatterns = [
    path('apply/step-1/', views.application_step_one_view, name='application-step-1'),
    path('apply/step-2/', views.application_step_two_view, name='application-step-2'),
    path('success/<uuid:pk>/', views.application_success_view, name='application-success'),
    path('pay/<uuid:pk>/', views.initiate_payment_view, name='initiate-payment'),
    path('webhook/razorpay/', views.razorpay_webhook_view, name='razorpay-webhook'),
    path('payment-confirmation/',views.payment_confirmation_view, name='payment-confirmation'),
    path('find-application/', find_application_view, name='find-application'),
    path('procedure/', admission_procedure_view, name='admission-procedure'),
    path('fee-structure/', fee_structure_view, name='fee-structure'),

   
    
]