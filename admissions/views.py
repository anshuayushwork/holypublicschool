# admissions/views.py


from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentParentForm, DocumentUploadForm # Import DocumentUploadForm
from .models import AdmissionApplication # Import the model
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import razorpay
import json
from .forms import StudentParentForm, DocumentUploadForm, ApplicationSearchForm # Add ApplicationSearchForm


def application_step_one_view(request):
    """
    Handles Step 1: Collecting Student and Parent details.
    """
    if request.method == 'POST':
        # Create a form instance with the submitted data and files
        form = StudentParentForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the form data to the model, but don't commit to the database yet
            application = form.save(commit=False)
            
            # Set the status to 'INCOMPLETE' to mark that step 1 is done
            application.status = 'INCOMPLETE'
            
            # Now, save the object to the database
            application.save()
            
            # Store the unique ID of this new application in the user's session
            # This is how we'll find it again in the next step
            request.session['application_uid'] = str(application.uid)
            
            # Redirect the user to the URL for step two
            return redirect('application-step-2')
    else:
        # If it's a GET request, just display a blank form
        form = StudentParentForm()

    return render(request, 'admissions/application_step_one.html', {'form': form})


def application_step_two_view(request):
    """
    Handles Step 2: Uploading documents and finalizing the application.
    """
    try:
        # 1. Retrieve the application UID that we stored in the session in step 1
        application_uid = request.session.get('application_uid')
        if not application_uid:
            # If the UID is not in the session, the user hasn't completed step 1.
            # Redirect them back to the start.
            return redirect('application-step-1')

        # 2. Get the application object from the database that is still 'INCOMPLETE'
        application = get_object_or_404(AdmissionApplication, uid=application_uid, status='INCOMPLETE')

    except (AdmissionApplication.DoesNotExist, KeyError):
        # Handle cases where the application might have been deleted or session is invalid
        return redirect('application-step-1')


    if request.method == 'POST':
        # Create a form instance, binding it to the existing application object
        # This tells Django to UPDATE this object, not create a new one.
        form = DocumentUploadForm(request.POST, request.FILES, instance=application)
        
        if form.is_valid():
            # Save the uploaded files to the application object
            updated_application = form.save(commit=False)
            
            # 3. Update the status to mark the application as fully submitted
            updated_application.status = 'PENDING_PAYMENT'
            updated_application.save()
            
            # 4. Clean up the session by deleting the UID
            del request.session['application_uid']
            
            # 5. Redirect to a success page (we will create this next)
            # We pass the UID so the success page can show the application ID
            return redirect('application-success', pk=updated_application.uid)
    else:
        # If it's a GET request, just display a blank document upload form
        form = DocumentUploadForm()

    return render(request, 'admissions/application_step_two.html', {'form': form})




def application_success_view(request, pk):
    """
    Displays a success message to the user after they submit the form.
    """
    # Get the specific application object using the primary key (pk) from the URL
    application = get_object_or_404(AdmissionApplication, pk=pk)
    
    # Render a template, passing the application object to it
    return render(request, 'admissions/application_success.html', {'application': application})



# admissions/views.py

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import razorpay
import json

# ... (your other imports and views) ...

def initiate_payment_view(request, pk):
    """
    Creates a Razorpay Order and renders the payment page.
    """
    application = get_object_or_404(AdmissionApplication, pk=pk)
    
    # Define your application fee. Let's assume it's ₹500 for now.
    application_fee = 500
    
    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Create an Order
    razorpay_order = client.order.create({
        "amount": application_fee * 100,  # Amount is in paise, so multiply by 100
        "currency": "INR",
        "receipt": str(application.uid),
        "notes": {"application_id": str(application.uid)}
    })
    
    # Save the order_id to your application model
    application.order_id = razorpay_order['id']
    application.save()
    
    context = {
        'application': application,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': application_fee * 100,
        'currency': 'INR',
    }
    
    return render(request, 'admissions/payment.html', context)



# admissions/views.py

@csrf_exempt
def razorpay_webhook_view(request):
    """
    Handles incoming webhooks from Razorpay to verify payments.
    """
    if request.method == "POST":
        try:
            # Get the webhook payload and signature
            # payload = request.body
            payload = request.body.decode('utf-8')
            signature = request.headers.get('X-Razorpay-Signature')
            
            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            # Verify the signature
            client.utility.verify_webhook_signature(payload, signature, settings.RAZORPAY_KEY_SECRET)
            
            # If verification is successful, process the event
            webhook_body = json.loads(payload)
            order_id = webhook_body['payload']['payment']['entity']['order_id']
            payment_id = webhook_body['payload']['payment']['entity']['id']
            
            # Find the application and update its status
            application = AdmissionApplication.objects.get(order_id=order_id)
            application.payment_id = payment_id
            application.status = 'COMPLETED'
            application.save()
            
            return HttpResponse(status=200)

        except (ValueError, KeyError, AdmissionApplication.DoesNotExist, razorpay.errors.SignatureVerificationError) as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Webhook verification FAILED!")
            print(f"Error Type: {type(e)}")
            print(f"Error Message: {e}")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return HttpResponse(status=400)
            
    
    return HttpResponse(status=405)



def payment_confirmation_view(request):
    """
    Displays a final confirmation page after successful payment.
    """
    return render(request, 'admissions/payment_confirmation.html')





def find_application_view(request):
    form = ApplicationSearchForm()
    if request.method == 'POST':
        form = ApplicationSearchForm(request.POST)
        if form.is_valid():
            app_number = form.cleaned_data['application_number']
            dob = form.cleaned_data['date_of_birth']

            try:
                # Look for an application that matches the details AND is pending payment
                application = AdmissionApplication.objects.get(
                    application_number__iexact=app_number,
                    date_of_birth=dob,
                    status='PENDING_PAYMENT'
                )
                # If found, redirect to the payment page we already built
                return redirect('initiate-payment', pk=application.uid)
            except AdmissionApplication.DoesNotExist:
                # If no match is found, add an error to the form
                form.add_error(None, "No pending application found with these details. Please check your input.")

    return render(request, 'admissions/find_application.html', {'form': form})


def admission_procedure_view(request):
    """
    Renders the admission procedure page.
    """
    return render(request, 'admissions/procedure.html')

def fee_structure_view(request):
    """
    Renders the fee structure page.
    """
    return render(request, 'admissions/fee_structure.html')