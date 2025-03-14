# Quiz Generator

This repository contains a Python script to generate multiple-choice quizzes based on provided notes. The script uses the Gemini API to create quizzes with different difficulty levels.

## Features

- Generate multiple-choice questions
- Supports three difficulty levels: Easy, Medium, and Hard
- Customizable number of questions
- Automatically formats quiz questions with four options and a correct answer

## How It Works

The `QuizGenerator` class interacts with the Gemini API to generate quizzes based on the provided notes. The following steps occur:

1. Initialization: The class is initialized with an API key and a model name.
2. Quiz Generation: The `generate_quiz()` or `generate_quiz_async()` methods send a request to the Gemini API, passing the required parameters like difficulty, number of questions, and notes.
3. API Response: The API returns a JSON-formatted response with questions, and the script validates and formats the output into a usable quiz structure.

## Usage

### Synchronous Example:

```python
from quiz_generator import QuizGenerator

api_key = "your_api_key_here"
generator = QuizGenerator(api_key)

difficulty = "medium"
num_questions = 5
notes = """A dog is a domesticated mammal from the species *Canis lupus familiaris*, 
known for its loyalty, intelligence, and companionship with humans."""

quiz = generator.generate_quiz(difficulty, num_questions, notes)
print(quiz)
