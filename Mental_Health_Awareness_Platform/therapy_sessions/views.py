from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ScheduleSessionForm
from .models import TherapySession
from payments.models import Payment  # Import your Payment model

@login_required
def schedule_session(request):
    if request.method == 'POST':
        form = ScheduleSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.client = request.user
            session.booked = True  # Set session as booked
            session.save()

            # Redirect to the checkout page with the newly created session ID
            return redirect('checkout', session_id=session.id)  # Redirect to checkout
    else:
        form = ScheduleSessionForm()
    return render(request, 'therapy_sessions/schedule.html', {'form': form})


@login_required
def session_list(request):
    # Get all sessions booked by the logged-in user (client)
    user_sessions = TherapySession.objects.filter(client=request.user).order_by('session_date')

    # Get available sessions (not booked and session date in the future)
    available_sessions = TherapySession.objects.filter(
        booked=False,  # Not booked
        session_date__gte=timezone.now()  # Date is today or in the future
    ).order_by('session_date')

    # Pass both booked and available sessions to the template
    return render(request, 'therapy_sessions/session_list.html', {
        'user_sessions': user_sessions,  # Sessions the user booked
        'available_sessions': available_sessions  # Sessions available for booking
    })

@login_required
def cancel_booking(request, session_id):
    # Get the session the user wants to cancel
    session = get_object_or_404(TherapySession, id=session_id, client=request.user)

    # Only allow cancellation if the session is booked by the current user
    if session.booked:
        session.booked = False
        session.client = None  # Clear the client field if it's linked to a user
        session.save()

    # Redirect back to the session list
    return redirect('session_list')

@login_required
def checkout(request, session_id):
    # Get the therapy session the user wants to pay for
    session = get_object_or_404(TherapySession, id=session_id)  # Ensure the session exists
    if request.method == 'POST':
        amount = session.calculate_price()  # Use the session price
        # Here you would integrate the payment gateway logic
        # For example, integrating with Stripe or PayPal to process the payment

        # If the payment is successful, create the payment record
        payment = Payment.objects.create(user=request.user, session=session, amount=amount)
        payment.status = 'Completed'  # Update payment status
        payment.save()

        return redirect('session_list')  # Redirect to the session list after payment
    return render(request, 'payments/checkout.html', {'session': session})  # Render checkout page
