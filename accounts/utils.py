import string
import secrets
import resend
import logging
from datetime import datetime

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from suppcoapi.settings import DOMAIN
from accounts.tokens import account_activation_token

logger = logging.getLogger(__name__)


current_year = datetime.now().year


def generate_reference():
    characters = string.ascii_letters + string.digits
    random_string = "".join(secrets.choice(characters) for _ in range(12))
    return random_string.upper()

def generate_username():
    year = datetime.now().year % 100
    random_number = "".join(secrets.choice(string.digits) for _ in range(6))


def send_activation_email(user):
    """
    Resend email integration
    """
    email_body = ""
    current_year = datetime.now().year

    try:
        email_body = render_to_string(
            "email_verification.html",
            {
                "user": user,
                "domain": DOMAIN,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
                "current_year": current_year,
            },
        )
        params = {
            "from": "SUPPCO <onboarding@corbantechnologies.org>",
            "to": [user.email],
            "subject": "Activate your account",
            "html": email_body,
        }
        response = resend.Emails.send(params)
        logger.info(f"Email sent to {user.email} with response: {response}")
        return response

    except Exception as e:
        logger.error(f"Error sending email to {user.email}: {str(e)}")
        return None


def send_account_creation_email(user):
    """
    A function to send a successful account creation email
    """
    email_body = ""
    current_year = datetime.now().year

    try:

        email_body = render_to_string(
            "account_created.html", {"user": user, "current_year": current_year}
        )
        params = {
            "from": "SUPPCO <onboarding@corbantechnologies.org>",
            "to": [user.email],
            "subject": "Welcome to SUPPCO",
            "html": email_body,
        }
        response = resend.Emails.send(params)
        logger.info(f"Email sent to {user.email} with response: {response}")
        return response

    except Exception as e:
        logger.error(f"Error sending email to {user.email}: {str(e)}")
        return None


def send_verification_email(user, verification_code):
    """
    A function to send a verification email
    """

    email_body = ""
    current_year = datetime.now().year

    try:
        email_body = render_to_string(
            "account_verification.html",
            {
                "user": user,
                "verification_code": verification_code,
                "current_year": current_year,
            },
        )
        params = {
            "from": "SUPPCO <onboarding@corbantechnologies.org>",
            "to": [user.email],
            "subject": "Verify your account",
            "html": email_body,
        }
        response = resend.Emails.send(params)
        logger.info(f"Email sent to {user.email} with response: {response}")
        return response

    except Exception as e:
        logger.error(f"Error sending email to {user.email}: {str(e)}")
        return None


def send_password_reset_email(user, verification_code):
    """
    A function to send a password reset email
    """
    email_body = ""
    current_year = datetime.now().year

    try:
        email_body = render_to_string(
            "password_reset.html",
            {
                "user": user,
                "verification_code": verification_code,
                "current_year": current_year,
            },
        )
        params = {
            "from": "SUPPCO <reset-password@corbantechnologies.org>",
            "to": [user.email],
            "subject": "Reset your password",
            "html": email_body,
        }
        response = resend.Emails.send(params)
        logger.info(f"Email sent to {user.email} with response: {response}")
        return response

    except Exception as e:
        logger.error(f"Error sending email to {user.email}: {str(e)}")
        return None
