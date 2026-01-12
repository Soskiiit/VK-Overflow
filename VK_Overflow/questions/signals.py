from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db.models import Sum
from django.db.models.functions import Coalesce

from core.sse_bridges import Centrifugo
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
            'author_avatar': instance.author.get_avatar_thumbnail(),
            'rating': instance.rating,
            'question_id': instance.question.id
        }

        Centrifugo.publish(instance.question.get_centrifuge_channel(), data)
