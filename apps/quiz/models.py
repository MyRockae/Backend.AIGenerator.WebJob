from django.db import models
from apps.account.models import User

class Quiz(models.Model):
    quiz_title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    number_of_questions = models.PositiveIntegerField(default=10)
    model_name = models.CharField(max_length=255, null=True, blank=True)
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('Easy', 'Easy'),('Medium', 'Medium'),('Hard', 'Hard')],
        default='Medium'
    )
    category = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)
    is_supervised = models.BooleanField(default=False)
    is_organization_only = models.BooleanField(default=False)
    is_timed = models.BooleanField(default=False)
    time_limit = models.FloatField(null=True, blank=True)
    auth_required = models.BooleanField(default=False)
    has_flash_card = models.BooleanField(default=False)

    def __str__(self):
        return self.quiz_title

    class Meta:
        db_table = 'Quiz'
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'



class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self):
        return self.text
    
    class Meta:
        db_table = 'question'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    label = models.CharField(max_length=1)  # A, B, C, etc.
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.label}: {self.text}"
    
    class Meta:
        db_table = 'answer_option'
        verbose_name = 'Answer Option'
        verbose_name_plural = 'Answer Options'