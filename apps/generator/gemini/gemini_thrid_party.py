import json
import re
import requests

def gemini_flash_2_0_api_quiz(api_key, num_questions, difficulty, notes):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    prompt = (
        f"Generate {num_questions} multiple-choice quiz questions about {notes} at a {difficulty} difficulty level. "
        "Each question should have exactly five answer options and a correct answer. "
        "Return the result in a valid JSON format without extra text, like this: \n"
        "{\n"
        '  "quiz": [\n'
        '    {"question": "Sample question?", "options": ["A", "B", "C", "D", "E"], "correct_answer": "A"}\n'
        "  ]\n"
        "}"
    )

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()

    if "candidates" in response_data and response_data["candidates"]:
        generated_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        extracted_json = re.sub(r"```json\n|\n```", "", generated_text).strip()

        try:
            quiz_data = json.loads(extracted_json)
            return quiz_data
        except json.JSONDecodeError:
            return {"error": "Failed to parse AI-generated response", "raw_response": extracted_json}
    
    return {"error": "No valid response from API"}


def gemini_flash_2_0_api_flashcard(api_key, num_cards, notes):
    """
    Calls the Gemini API to generate flashcard items.
    Expects the API to return JSON data like:
    {
      "flashcards": [
          {"question": "Sample question?", "answer": "Sample answer."}
      ]
    }
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    
    prompt = (
        f"Generate {num_cards} flashcard items about {notes}. "
        "Each flashcard item should have a 'question' and an 'answer'. "
        "Return the result in a valid JSON format without extra text, like this: \n"
        "{\n"
        '  "flashcards": [\n'
        '    {"question": "Sample question?", "answer": "Sample answer."}\n'
        "  ]\n"
        "}"
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    
    if "candidates" in response_data and response_data["candidates"]:
        generated_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        # Remove markdown formatting if present
        extracted_json = re.sub(r"```json\n|\n```", "", generated_text).strip()
        try:
            flashcard_data = json.loads(extracted_json)
            return flashcard_data
        except json.JSONDecodeError:
            return {"error": "Failed to parse AI-generated response", "raw_response": extracted_json}
    
    return {"error": "No valid response from API"}

