# In urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:session_id>/', views.checkout, name='checkout'),
    path('confirm_payment/<int:session_id>/', views.confirm_payment, name='confirm_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failed/<int:session_id>/', views.payment_failed, name='payment_failed'),  # Updated to include session_id
]
