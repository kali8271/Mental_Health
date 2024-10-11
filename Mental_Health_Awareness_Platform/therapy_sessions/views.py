from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ScheduleSessionForm
from .models import TherapySession
from payments.models import Payment  # Import your Payment model

@login_required
def schedule_session(request):
    if request.method == 'POST':
        form = ScheduleSessionForm(request.POST, user=request.user)  # Pass the user to the form
        if form.is_valid():
            session = form.save(commit=False)
            session.client = request.user  # Assign the logged-in user as the client
            session.booked = True  # Mark the session as booked
            session.save()

            # Redirect to the checkout page with the newly created session ID
            return redirect('checkout', session_id=session.id)
    else:
        form = ScheduleSessionForm(user=request.user)  # Pass the user to the form

    return render(request, 'therapy_sessions/schedule.html', {'form': form})

@login_required
def session_list(request):
    """
    View to display a list of therapy sessions.
    Shows booked sessions and available sessions for the logged-in user.
    """
    user_sessions = TherapySession.objects.filter(client=request.user).order_by('session_date')
    available_sessions = TherapySession.objects.filter(
        booked=False,  # Not booked
        session_date__gte=timezone.now()  # Date is today or in the future
    ).order_by('session_date')

    return render(request, 'therapy_sessions/session_list.html', {
        'user_sessions': user_sessions,
        'available_sessions': available_sessions
    })


@login_required
def cancel_booking(request, session_id):
    """
    View to cancel a booked therapy session.
    Only allows cancellation for sessions booked by the current user.
    """
    session = get_object_or_404(TherapySession, id=session_id, client=request.user)

    if session.booked:
        session.booked = False
        session.client = None  # Clear the client field
        session.save()

    return redirect('session_list')


@login_required
def checkout(request, session_id):
    """
    View for handling the payment process for a booked session.
    Integrates with a payment gateway and processes payments.
    """
    session = get_object_or_404(TherapySession, id=session_id)
    if request.method == 'POST':
        amount = session.calculate_price()  # Calculate the price for the session
        
        # Here you would integrate the payment gateway logic
        try:
            # Example: Replace this with actual payment processing code
            # payment_success = process_payment(amount)
            payment_success = True  # Simulate successful payment for example
            
            if payment_success:
                payment = Payment.objects.create(user=request.user, session=session, amount=amount)
                payment.status = 'Completed'  # Update payment status
                payment.save()
                return redirect('session_list')  # Redirect to the session list after successful payment
            else:
                # Handle payment failure
                return render(request, 'payments/checkout.html', {
                    'session': session,
                    'error': 'Payment failed. Please try again.'
                })

        except Exception as e:
            # Log the exception or handle it as needed
            return render(request, 'payments/checkout.html', {
                'session': session,
                'error': f'An error occurred during payment: {str(e)}'
            })

    return render(request, 'payments/checkout.html', {'session': session})  # Render the checkout page
