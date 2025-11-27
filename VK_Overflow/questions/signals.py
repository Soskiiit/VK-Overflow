from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db.models import Sum
from django.db.models.functions import Coalesce

from questions.models import AnswerGrade, QuestionGrade


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
