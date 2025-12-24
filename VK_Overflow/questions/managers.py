from django.apps import apps
from django.db import models
from django.db.models.functions import Coalesce


# Расположены в managers.py ибо используем их .as_manager()
class AnswerQuerySet(models.QuerySet):
    def with_votes_from(self, user):
        # Чтоб избежать циклических импортов
        AnswerGrade = apps.get_model('questions', 'AnswerGrade')
        if not user.is_authenticated:
            return self.annotate(
                user_vote=models.Value(0, output_field=models.IntegerField())
            )
        return self.annotate(
            user_vote=Coalesce(
                models.Subquery(
                    AnswerGrade.objects.filter(
                        answer=models.OuterRef('pk'),
                        author=user
                    ).values('grade')[:1]
                ),
                models.Value(0),
                output_field=models.IntegerField()
            )
        )


class QuestionQuerySet(models.QuerySet):
    def with_votes_from(self, user):
        if user.is_authenticated:
            QuestionGrade = apps.get_model('questions', 'QuestionGrade')
            return self.annotate(
                user_vote=Coalesce(
                    models.Subquery(
                        QuestionGrade.objects.filter(
                            question=models.OuterRef('pk'),
                            author=user
                        ).values('grade')[:1]
                    ),
                    models.Value(0),
                    output_field=models.IntegerField()
                )
            )
        return self.annotate(user_vote=models.Value(0, output_field=models.IntegerField()))
