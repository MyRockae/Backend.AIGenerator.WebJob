from rest_framework import serializers

class SuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()

class EmailRecipientSerializer(serializers.Serializer):
    """Serializer for recipient details"""
    name = serializers.CharField(required=True, max_length=255)
    email = serializers.EmailField(required=True)

class SendVerificationEmailSerializer(serializers.Serializer):
    """Serializer for the verification email request"""
    subject = serializers.CharField(default="Welcome to Rockea", max_length=255)
    body = serializers.CharField()
    to = EmailRecipientSerializer(many=True)

class StandardSuccessResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    message = serializers.CharField(default="Successfully Completed", max_length=255)