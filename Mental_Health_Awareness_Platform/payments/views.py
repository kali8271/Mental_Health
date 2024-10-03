from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Payment
from therapy_sessions.models import TherapySession  # Adjust this import based on your actual model location
from django.conf import settings

@login_required
def checkout(request, session_id):
    session = get_object_or_404(TherapySession, id=session_id)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        amount = session.price  # Assume there's a price field in the TherapySession model

        # Create the payment record (consider storing the payment_method too)
        payment = Payment.objects.create(user=request.user, session=session, amount=amount)

        # Integrate payment gateway here (e.g., Stripe, PayPal, etc.)
        # If payment is successful:
        payment.status = 'Completed'
        payment.save()

        return redirect('session_list')  # Redirect to session list after successful payment

    return render(request, 'payments/checkout.html', {'session': session})
