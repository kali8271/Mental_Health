from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment
from therapy_sessions.models import Session  # Assuming you have a Session model
from django.conf import settings

@login_required
def checkout(request, session_id):
    session = Session.objects.get(id=session_id)
    if request.method == 'POST':
        amount = session.price  # Assume there's a price field in the Session model
        payment = Payment.objects.create(user=request.user, session=session, amount=amount)
        # Integrate payment gateway here (like Stripe, PayPal, etc.)
        # If payment is successful:
        payment.status = 'Completed'
        payment.save()
        return redirect('session_list')  # Redirect to session list after successful payment
    return render(request, 'payments/checkout.html', {'session': session})
