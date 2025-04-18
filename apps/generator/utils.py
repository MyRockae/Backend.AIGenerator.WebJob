from rest_framework import status
from apps.subscription.models import UserSubscription
from apps.shared.models import CustomWebApiException

def check_generative_ai_usage(user, num_questions, notes, max_questions=100, max_notes_length=15000):
    try:
        subscription = UserSubscription.objects.get(user=user)
    except UserSubscription.DoesNotExist:
        raise CustomWebApiException(error="No subscription found for user",code=status.HTTP_400_BAD_REQUEST)

    # Check if the subscription plan is free (case insensitive check)
    if subscription.plan.name.lower() == "free":
        if num_questions > max_questions:
            raise CustomWebApiException(error=f"Free subscription allows a maximum of {max_questions} questions.",code=status.HTTP_400_BAD_REQUEST)
        if len(notes) > max_notes_length:
            raise CustomWebApiException(error=f"Free subscription notes cannot exceed {max_notes_length} characters.",code=status.HTTP_400_BAD_REQUEST)
        
def validate_inputs(num_questions, difficulty, notes, requested_ai_model):
    # Check if num_questions is greater than 0
    if num_questions <= 0:
        raise ValueError("num_questions must be greater than 0.")
    
    # Check if difficulty is among easy, medium, or hard (case insensitive)
    valid_difficulties = {"easy", "medium", "hard"}
    if difficulty.lower() not in valid_difficulties:
        raise ValueError("difficulty must be 'easy', 'medium', or 'hard' (case insensitive).")
    
    # Check if notes is not empty or whitespace
    if not notes or not notes.strip():
        raise ValueError("notes must not be empty or whitespace.")
    
    # Check if requested_ai_model is not empty or whitespace
    if not requested_ai_model or not requested_ai_model.strip():
        raise ValueError("requested_ai_model must not be empty.")
    
    return True
        