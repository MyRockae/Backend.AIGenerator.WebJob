import requests
from django.conf import settings
from apps.shared.models import InternalServerError
from apps.shared.serializers import SendVerificationEmailSerializer

def send_email(subject, body, recipients):
    # Initialize email data using the serializer
    email_serializer = SendVerificationEmailSerializer(data={
        "subject": subject,
        "body": body,
        "to": recipients
    })

    # Validate the email data
    email_serializer.is_valid(raise_exception=True)

    # Send email via SMTP API
    response = requests.post(
        settings.SMTP_SEND_MAIL_URL,
        json=email_serializer.validated_data,
        headers={"Authorization": f"Bearer {settings.SMTP_API_KEY}"}
    )

    # Check if the email was sent successfully
    if response.status_code != 200:
        raise InternalServerError(f"Failed to send email: {response.text}")

    return {"message": "Email sent successfully."}
