from django.urls import path
from . import views

app_name = 'Payments'

urlpatterns = [
    path('verify_smartcard/', views.verify_smartcard, name='verify_smartcard'),
    path('purchase_product/', views.purchase_product, name='purchase_product'),
    path('subscription_form/', views.subscription_form, name='subscription_form'),
    
]



