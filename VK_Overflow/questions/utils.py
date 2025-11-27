from django.db.models import OuterRef, Subquery, Sum, Value
from django.db.models.functions import Coalesce

from questions.models import Answer, AnswerGrade, Question, QuestionGrade


def recalculate_question_ratings(*args):
    rating_subquery = Subquery(
        QuestionGrade.objects.filter(
            question=OuterRef('pk')
        ).values(
            'question'  # Группируем по вопросу
        ).annotate(
            total=Sum('grade')
        ).values('total')
    )

    Question.objects.update(
        rating=Coalesce(rating_subquery, Value(0))  # if NULL -> 0
    )


def recalculate_answer_ratings(*args):
    rating_subquery = Subquery(
        AnswerGrade.objects.filter(
            answer=OuterRef('pk')
        ).values(
            'answer'  # Группируем по ответу
        ).annotate(
            total=Sum('grade')
        ).values('total')
    )

    Answer.objects.update(
        rating=Coalesce(rating_subquery, Value(0))  # if NULL -> 0
    )
