from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Payment
from therapy_sessions.models import TherapySession
import razorpay  # Razorpay SDK for server-side

# Razorpay client configuration
razorpay_client = razorpay.Client(auth=('your_razorpay_key', 'your_razorpay_secret'))

@login_required
def checkout(request, session_id):
    session = get_object_or_404(TherapySession, id=session_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        amount = session.calculate_price() * 100  # Convert to paise for Razorpay (INR currency)

        if payment_method == 'razorpay':
            razorpay_order = razorpay_client.order.create({
                "amount": amount,
                "currency": "INR",
                "payment_capture": '1'  # Auto capture payment after confirmation
            })

            order_id = razorpay_order['id']

            return render(request, 'payments/checkout.html', {
                'session': session,
                'razorpay_key': 'your_razorpay_key',
                'amount': amount,
                'order_id': order_id
            })

    return render(request, 'payments/checkout.html', {'session': session})


@login_required
def confirm_payment(request, session_id):
    session = get_object_or_404(TherapySession, id=session_id)

    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        try:
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            razorpay_client.utility.verify_payment_signature(params_dict)

            payment = Payment.objects.create(
                user=request.user,
                session=session,
                amount=session.calculate_price(),
                status='Completed',
                payment_id=payment_id,
                order_id=order_id
            )
            return redirect('payment_success')
        except razorpay.errors.SignatureVerificationError:
            return redirect('payment_failed', session_id=session.id)


@login_required
def payment_success(request):
    return render(request, 'payments/payment_success.html')


@login_required
def payment_failed(request, session_id):
    session = get_object_or_404(TherapySession, id=session_id)
    return render(request, 'payments/payment_failed.html', {'session': session})
