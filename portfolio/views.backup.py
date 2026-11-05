from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.shortcuts import redirect, render

CONTACT_RECIPIENT = "atimangojoan85@gmail.com"


def portfolio_home(request):
    if request.method == "POST":
        back = f"{request.path}#contact"

        # Honeypot: bots fill this hidden field, people never see it
        if request.POST.get("website"):
            return redirect(back)

        name = request.POST.get("name", "").strip()[:100]
        email = request.POST.get("email", "").strip()[:150]
        subject = request.POST.get("subject", "").strip()[:150] or "New message"
        body = request.POST.get("message", "").strip()[:3000]

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return redirect(back)

        if not (name and body):
            messages.error(request, "Please fill in your name and message.")
            return redirect(back)

        try:
            EmailMessage(
                subject=f"[Portfolio] {subject}",
                body=f"From: {name} <{email}>\n\n{body}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[CONTACT_RECIPIENT],
                reply_to=[email],
            ).send(fail_silently=False)
            messages.success(request, "Thank you! Your message was sent. I'll get back to you soon.")
        except Exception:
            messages.error(request, "Sorry, the message could not be sent. Please email me directly.")

        return redirect(back)

    return render(request, "home.html")  # use your own template path

# urls.py uses both names for the same page
home = portfolio_home
