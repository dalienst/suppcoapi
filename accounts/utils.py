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
    random_number = "".join(secrets.choice(string.digits) for _ in range(10))
    return f"suppco{year}{random_number}"


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


def send_employee_added_email(user, employee, temporary_password):
    """
    Send an email to an employee notifying them they have been added to a company,
    including their login credentials and activation link.

    Args:
        user: The company owner (User instance) who added the employee.
        employee: The employee (User instance) being notified.
        temporary_password: The temporary password set for the employee.

    Returns:
        The response from the email service, or None if sending fails.
    """
    try:
        # Get the employment record to access company and role
        employment = employee.employment.filter(is_active=True).first()
        if not employment:
            raise ValueError("No active employment found for the employee.")

        # Prepare context for the email template
        email_body = render_to_string(
            "employee_added.html",
            {
                "owner": user,
                "employee": employee,
                "company": employment.company,
                "role": employment.role,
                "temporary_password": temporary_password,
                "domain": DOMAIN,
                "uid": urlsafe_base64_encode(force_bytes(employee.pk)),
                "token": account_activation_token.make_token(employee),
                "current_year": current_year,
                "site": employee.assigned_site,
                "branch": employee.assigned_branch,
            },
        )
        params = {
            "from": "SUPPCO <onboarding@corbantechnologies.org>",
            "to": [employee.email],
            "subject": f"Welcome to {employment.company.name} - Your Account Details",
            "html": email_body,
        }
        response = resend.Emails.send(params)
        logger.info(
            f"Employee added email sent to {employee.email} with response: {response}"
        )
        return response

    except Exception as e:
        logger.error(
            f"Error sending employee added email to {employee.email}: {str(e)}"
        )
        return None
