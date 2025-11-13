our admin panel is complete content management system where an administrator can manage:

Site-wide settings and homepage content

Faculty profiles

News, events, and circulars

Photo albums and galleries

Academic departments and documents


admissions workflow
Step 1: Create Two Forms (forms.py)
You'll have a form for each part of the application.

StudentParentForm: This will contain all the fields from the "Student and Parent Details" section.

DocumentUploadForm: This form will handle the file uploads for Part 2 (e.g., Birth Certificate, Previous Marksheet, etc.).

Step 2: Create Two Views (views.py)
application_step_one_view:

When a user submits this form, the view validates the data.

If valid, it does not save to the database. Instead, it stores all the form data in request.session.

It then redirects the user to the URL for step two.

application_step_two_view:

This view first checks if the data from step one exists in the session.

It displays the document upload form.

When the user submits the documents, this view:

Retrieves the data from the session.

Combines it with the newly uploaded files.

Creates the final AdmissionApplication object and saves everything to the database at once.

Clears the data from the session.

Redirects to the final "Success / Pay Now" page.

Step 3: Update URLs (urls.py)




from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
from .models import AdmissionApplication

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def initiate_payment(request, pk):
    """
    View to create a Razorpay order and render the payment page.
    """
    application_obj = get_object_or_404(AdmissionApplication, pk=pk)
    
    # Define payment amount (example: Rs. 500)
    payment_amount = 50000 # Amount in paise (500 * 100)

    # Create Razorpay Order
    razorpay_order = client.order.create({
        "amount": payment_amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    # Save the order_id to your application model
    application_obj.razorpay_order_id = razorpay_order['id']
    application_obj.save()
    
    context = {
        'application': application_obj,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': payment_amount,
    }
    return render(request, 'admissions/payment.html', context)


@csrf_exempt
def webhook_handler(request):
    """
    Handles incoming webhooks from Razorpay to securely verify payment.
    This is the ONLY reliable way to confirm a payment.
    """
    if request.method == "POST":
        try:
            # Get the signature from the request header
            signature = request.headers.get('x-razorpay-signature')
            
            # Verify the signature
            client.utility.verify_webhook_signature(request.body, signature, settings.RAZORPAY_WEBHOOK_SECRET)
            
            # If verification is successful, process the payload
            payload = request.POST
            razorpay_order_id = payload.get('payload[payment][entity][order_id]')
            
            # Find the application and update its status
            application_obj = AdmissionApplication.objects.get(razorpay_order_id=razorpay_order_id)
            application_obj.is_paid = True # Or update your status field
            application_obj.razorpay_payment_id = payload.get('payload[payment][entity][id]')
            application_obj.save()

            return JsonResponse({'status': 'ok'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error'}, status=400)


def payment_success_page(request):
    """
    A simple "Thank You" page shown to the user after they are redirected.
    This view DOES NOT update the database. It's just for user feedback.
    """
    return render(request, 'admissions/payment_success.html')



    