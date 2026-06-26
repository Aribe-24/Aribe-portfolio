from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

# Create your views here.
def home(request):
    return render(request, 'home.html')


def portfolio_home(request):
    if request.method == "POST":
        # Extract and strip whitespace from form fields
        name = request.POST.get('name', '').strip()
        sender_email = request.POST.get('email', '').strip()
        message_body = request.POST.get('message', '').strip()
        
        # Simple validation block to prevent sending empty emails
        if not name or not sender_email or not message_body:
            messages.error(request, "Please fill in all required fields.")
            return redirect('/#contact')
        
        # Format the email layout cleanly
        email_subject = f"💼 New Portfolio Inquiry from {name}"
        email_message = (
            f"You received a new message from your portfolio website contact form:\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Sender Name:  {name}\n"
            f"Sender Email: {sender_email}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"Message:\n"
            f"{message_body}\n"
        )
        
        try:
            # Trigger the Django email dispatch
            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['atimangojoan85@gmail.com'],  # Your destination inbox
                fail_silently=False,
            )
            # Adds a standard 'success' tag to Django's messages framework
            messages.success(request, "Your message has been sent successfully! I will get back to you soon.")
        except Exception as e:
            # Adds an 'error' tag if email server fails (e.g., bad SMTP configuration)
            messages.error(request, "Oops! Something went wrong while sending your message. Please try again later.")
            # Optional: print(f"Mail Server Error: {e}") for local terminal debugging
            
        return redirect('/#contact')  # Redirects back to the contact anchor section

    # If GET request, just render the normal portfolio landing page
    return render(request, 'index.html')