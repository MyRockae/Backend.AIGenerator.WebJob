from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db import transaction

from .gemini_thrid_party import gemini_flash_2_0_api_quiz, gemini_flash_2_0_api_flashcard
from ..utils import check_generative_ai_usage
from apps.quiz.models import Quiz, Question, AnswerOption
from apps.flashcard.models import Flashcard, FlashcardItem

def gemini_flash_2_0_quiz_generator(user, quiz_id, num_questions, difficulty, notes):

    # Check AI usage limits
    check_generative_ai_usage(user=user, num_questions=num_questions, notes=notes)

    # Retrieve quiz instance
    quiz_instance = get_object_or_404(Quiz, pk=quiz_id)

    # Generate quiz data from API
    api_key = settings.GOOGLE_GENERATIVE_LANGUAGE_API_KEY
    quiz_data = gemini_flash_2_0_api_quiz(api_key, num_questions, difficulty, notes)

    # Validate API response
    if not quiz_data or 'quiz' not in quiz_data:
        return {"status": "error", "message": "Invalid response from AI API"}

    questions_to_create = []
    answer_options_to_create = []

    with transaction.atomic():
        for question_data in quiz_data.get('quiz', []):
            question_text = question_data.get('question', '').strip()
            options = question_data.get('options', [])
            correct_answer_text = question_data.get('correct_answer', '').strip().lower()

            if not question_text or len(options) != 5:
                continue  # Skip invalid questions

            # Create question instance
            question_instance = Question(quiz=quiz_instance, text=question_text)
            questions_to_create.append(question_instance)

        # Bulk create questions and assign their IDs
        created_questions = Question.objects.bulk_create(questions_to_create)

        for question_instance, question_data in zip(created_questions, quiz_data.get('quiz', [])):
            correct_option_instance = None

            for index, option in enumerate(question_data.get('options', [])):
                option_text = option.strip()
                label = chr(65 + index)  # 'A', 'B', 'C', etc.

                option_instance = AnswerOption(
                    question=question_instance,
                    label=label,
                    text=option_text,
                    is_correct=(option_text.lower() == question_data.get('correct_answer', '').strip().lower())
                )

                if option_instance.is_correct:
                    correct_option_instance = option_instance

                answer_options_to_create.append(option_instance)

        # Bulk create answer options
        AnswerOption.objects.bulk_create(answer_options_to_create)

    return {
        "status": "success",
        "message": f"Added {len(created_questions)} questions to the quiz",
        "quiz_id": quiz_id,
    }



def gemini_flash_2_0_flashcard_generator(user, flashcard_id, num_cards, notes):
    """
    Generates flashcard items using the Gemini API and saves them to a Flashcard.
    
    Parameters:
      - user: the authenticated user
      - flashcard_id: ID of the Flashcard instance to add items to
      - num_cards: number of flashcard items to generate
      - notes: the subject notes for generating the flashcard items
    
    Returns a dict with status and message.
    """
    # Check generative AI usage limits
    check_generative_ai_usage(user=user, num_questions=num_cards, notes=notes)
    
    # Retrieve flashcard instance (ensuring the flashcard belongs to the user)
    flashcard_instance = get_object_or_404(Flashcard, pk=flashcard_id, user=user)
    
    # Call the API to generate flashcard data
    api_key = settings.GOOGLE_GENERATIVE_LANGUAGE_API_KEY
    flashcard_data = gemini_flash_2_0_api_flashcard(api_key, num_cards, notes)
    
    # Validate API response
    if not flashcard_data or 'flashcards' not in flashcard_data:
        return {"status": "error", "message": "Invalid response from AI API"}
    
    items_to_create = []
    
    with transaction.atomic():
        for item_data in flashcard_data.get('flashcards', []):
            question_text = item_data.get('question', '').strip()
            answer_text = item_data.get('answer', '').strip()
            
            if not question_text or not answer_text:
                continue  # Skip invalid items
            
            # Create a FlashcardItem instance (not saved yet)
            item_instance = FlashcardItem(
                flashcard=flashcard_instance,
                question=question_text,
                answer=answer_text
            )
            items_to_create.append(item_instance)
        
        # Bulk create flashcard items
        FlashcardItem.objects.bulk_create(items_to_create)
    
    return {
        "status": "success",
        "message": f"Added {len(items_to_create)} flashcard items to flashcard {flashcard_id}.",
        "flashcard_id": flashcard_id,
    }



def gemini_flash_2_0_flashcard_auto_generator(quiz_id, num_items):
    # Retrieve all questions for the quiz.
    questions = Question.objects.filter(quiz_id=quiz_id)
    # Combine question texts into one string (one question per line).
    notes = "\n".join([q.text for q in questions if q.text])
    # Retrieve the API key from settings.
    api_key = settings.GOOGLE_GENERATIVE_LANGUAGE_API_KEY
    # Call the Gemini API function with the combined notes.
    flashcard_data = gemini_flash_2_0_api_flashcard(api_key, num_items, notes)
    # Validate API response
    if not flashcard_data or 'flashcards' not in flashcard_data:
        return {"status": "error", "message": "Invalid response from AI API"}
    
    # Retrieve the quiz instance.
    quiz_instance = get_object_or_404(Quiz, pk=quiz_id)
    
    # Use the quiz title as the flashcard title.
    flashcard_title = quiz_instance.quiz_title
    # Use auto generated description for the quiz.
    flashcard_description = f"Auto generated for {flashcard_title}"
    
    # Create a new Flashcard instance.
    flashcard_instance = Flashcard.objects.create(
        title=flashcard_title,
        description=flashcard_description,
        user=quiz_instance.user,
        quiz=quiz_instance
    )
    
    # Process the returned flashcard data to create flashcard items.
    flashcard_items = []
    for item in flashcard_data.get('flashcards', []):
        question_text = item.get('question', '').strip()
        answer_text = item.get('answer', '').strip()
        if question_text and answer_text:
            flashcard_item = FlashcardItem(
                flashcard=flashcard_instance,
                question=question_text,
                answer=answer_text
            )
            flashcard_items.append(flashcard_item)
    
    # Bulk create flashcard items.
    FlashcardItem.objects.bulk_create(flashcard_items)
    
    # Update the flashcard's number_of_flashcards field.
    flashcard_instance.number_of_flashcards = len(flashcard_items)
    flashcard_instance.save()
    
    return {
        "status": "success",
        "message": f"Added {len(flashcard_items)} flashcard items to flashcard {flashcard_instance.id}.",
        "flashcard_id": flashcard_instance.id,
    }

    
