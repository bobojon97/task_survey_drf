from django.db import models
from datetime import date
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Participant(models.Model):
    full_name = models.TextField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.id}'

class Schema(models.Model):
    name = models.CharField(max_length=150)
    start_data = models.DateField(default=date.today, editable=False)
    end_data = models.DateField(default=date.today)
    description = models.TextField()

    class Meta:
        ordering = ['-start_data']

    def __str__(self) -> str:
        return self.name


class Survey(models.Model):
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-schema']

    def __str__(self):
        return f'{self.scheme.name} - {self.participant}'

class Question(models.Model):
    ANSWER_TYPES = (
        ('TEXT', ('ответ текстом')),
        ('SINGLE', ('ответ с выбором одного варианта')),
        ('MULTIPLE', ('ответ с выбором нескольких вариантов')),
    )
    text = models.CharField(max_length=150)
    answer_type = models.CharField(choices=ANSWER_TYPES, default='TEXT', max_length=150)

    def __str__(self):
        return self.text

class AnswerOption(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.ForeignKey)

    def __str__(self) -> str:
        return self.text

class SchemaQuestion(models.Model):
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('schema', 'question')

class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('survey', 'question')

class Answer(models.Model):
    content = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.content

class AnswerQuestion(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('answer', 'question')

class SurveyAnswer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('survey', 'answer')

