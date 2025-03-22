from rest_framework import serializers

class AIQuizGeneratorRequestSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    num_questions = serializers.IntegerField(min_value=1)
    difficulty = serializers.CharField()
    notes = serializers.CharField()
    file = serializers.FileField(required=False)


class GeneratedQuizQuestionSerializer(serializers.Serializer):
    question = serializers.CharField()
    options = serializers.ListField(child=serializers.CharField())
    correct_answer = serializers.CharField()

class AIQuizSerializer(serializers.Serializer):
    quiz = GeneratedQuizQuestionSerializer(many=True)


class AIFlashcardGeneratorRequestSerializer(serializers.Serializer):
    flashcard_id = serializers.IntegerField()
    num_cards = serializers.IntegerField(min_value=1)
    notes = serializers.CharField()


class AIFlashcardAutoGeneratorRequestSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    num_items = serializers.IntegerField(min_value=1)