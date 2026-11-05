import logging

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .models import ContactMessage

logger = logging.getLogger(__name__)

CONTACT_RECIPIENT = "atimangojoan85@gmail.com"
THANKS = "Thank you! Your message was received. I'll get back to you soon."


def _reply(request, ok, text):
    """JSON for the page's fetch() call, or a normal redirect if JavaScript is off."""
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": ok, "message": text}, status=200 if ok else 400)
    (messages.success if ok else messages.error)(request, text)
    return redirect(f"{request.path}#contact")


def portfolio_home(request):
    if request.method == "POST":
        # Honeypot: bots fill this hidden field, people never see it
        if request.POST.get("website"):
            return _reply(request, True, THANKS)

        name = request.POST.get("name", "").strip()[:100]
        email = request.POST.get("email", "").strip()[:150]
        subject = request.POST.get("subject", "").strip()[:150]
        body = request.POST.get("message", "").strip()[:3000]

        try:
            validate_email(email)
        except ValidationError:
            return _reply(request, False, "Please enter a valid email address.")

        if not (name and body):
            return _reply(request, False, "Please fill in your name and message.")

        # 1) Always keep the message (visible in /admin/), so nothing is lost
        entry = ContactMessage.objects.create(
            name=name, email=email, subject=subject, message=body
        )

        # 2) Then try to email it; a failure is logged in the terminal, not shown to visitors
        try:
            EmailMessage(
                subject=f"[Portfolio] {subject or 'New message'}",
                body=f"From: {name} <{email}>\n\n{body}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[CONTACT_RECIPIENT],
                reply_to=[email],
            ).send(fail_silently=False)
            entry.emailed = True
            entry.save(update_fields=["emailed"])
        except Exception:
            logger.exception("Contact form: saved the message but the email could not be sent")

        return _reply(request, True, THANKS)

    return render(request, "home.html")


# urls.py in this project uses both names for the same page
home = portfolio_home
