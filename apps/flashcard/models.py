from django.db import models
from apps.account.models import User  # Adjust the import as per your project structure
from apps.quiz.models import Quiz       # Optional relation if a flashcard is linked to a quiz

class Flashcard(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    number_of_flashcards = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='flashcards'
    )
    # Use OneToOneField to ensure a quiz can have only one flashcard.
    quiz = models.OneToOneField(
        Quiz,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='flashcard'
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'flashcard'
        verbose_name = 'Flashcard'
        verbose_name_plural = 'Flashcards'


class FlashcardItem(models.Model):
    flashcard = models.ForeignKey(
        Flashcard,
        on_delete=models.CASCADE,
        related_name='items'
    )
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        # Returns a short preview of the question
        return f"{self.question[:50]}..."

    class Meta:
        db_table = 'flashcard_item'
        verbose_name = 'Flashcard Item'
        verbose_name_plural = 'Flashcard Items'
