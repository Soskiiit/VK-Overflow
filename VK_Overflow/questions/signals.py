import json
import urllib.request

from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db.models import Sum
from django.db.models.functions import Coalesce

from questions.models import Answer, AnswerGrade, QuestionGrade


@receiver(post_save, sender=QuestionGrade)
@receiver(post_delete, sender=QuestionGrade)
def update_question_rating(sender, instance, **kwargs):
    question = instance.question

    new_rating = question.questiongrade_set.aggregate(
        total=Coalesce(Sum('grade'), 0)
    )['total']

    question.rating = new_rating
    question.save(update_fields=['rating'])


@receiver(post_save, sender=AnswerGrade)
@receiver(post_delete, sender=AnswerGrade)
def update_answer_rating(sender, instance, **kwargs):
    answer = instance.answer

    new_rating = answer.answergrade_set.aggregate(
        total=Coalesce(Sum('grade'), 0)
    )['total']

    answer.rating = new_rating
    answer.save(update_fields=['rating'])


@receiver(post_save, sender=Answer)
def notify_new_answer(sender, instance, created, **kwargs):
    if created:
        data = {
            'id': instance.id,
            'text': instance.answer_text,
            'author': str(instance.author) if instance.author else 'Удалённый пользователь',
            'author_avatar': instance.author.avatar.url
            if instance.author and instance.author.avatar else '/static/assets/default-avatar.png',
            'rating': instance.rating,
            'question_id': instance.question.id
        }

        payload = {
            'method': 'publish',
            'params': {
                'channel': f'question_{instance.question.id}',
                'data': data
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'apikey {settings.CENTRIFUGO_API_KEY}'
        }

        try:
            req = urllib.request.Request(
                settings.CENTRIFUGO_API_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers
            )
            urllib.request.urlopen(req)
        except Exception as e:
            print(f"Failed to publish to Centrifugo: {e}")
