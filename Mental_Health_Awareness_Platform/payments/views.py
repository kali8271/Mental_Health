from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Payment
from therapy_sessions.models import TherapySession

@login_required
def checkout(request, session_id):
    # Get the therapy session the user wants to pay for
    session = get_object_or_404(TherapySession, id=session_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')  # If using payment methods like Stripe, PayPal

        # Calculate the amount based on the session's duration
        amount = session.calculate_price()  # Use the dynamic pricing based on duration

        # Create the payment record
        payment = Payment.objects.create(user=request.user, session=session, amount=amount)

        # Integrate the payment gateway logic here
        # For example, using Stripe, PayPal, etc., for payment processing

        # If payment is successful, update the payment status
        payment.status = 'Completed'
        payment.save()

        return redirect('session_list')  # Redirect to session list after successful payment

    return render(request, 'payments/checkout.html', {'session': session})
