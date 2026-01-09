from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.urls import reverse

from users.models import User
from .managers import AnswerQuerySet, QuestionQuerySet


class Tag(models.Model):
    COLOR_CHOICES = (
        ('grey', 'grey'),
        ('blue', 'blue'),
        ('green', 'green'),
        ('cyan', 'cyan'),
    )

    name = models.CharField(max_length=32, unique=True, verbose_name='Название тега')
    color = models.CharField(
        max_length=32,
        choices=COLOR_CHOICES,
        default='grey',
        verbose_name='Цвет тега'
    )

    def __str__(self):
        return f'Тэг "{self.name}"'

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Question(models.Model):
    objects = QuestionQuerySet.as_manager()  # гптшка с gemini'кой сказали, что эт best practices

    title = models.CharField(max_length=120, verbose_name='Заголовок')
    author = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='questions', verbose_name='Задан пользователем'
    )
    question_text = models.TextField(blank=True, verbose_name='Детали вопроса', max_length=6000)
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    best_answer = models.OneToOneField(
        'Answer',
        null=True, blank=True, on_delete=models.SET_NULL,
        related_name='best_for', verbose_name='Лучший ответ'
    )
    # индексируем в дб во имя страницы hot
    rating = models.IntegerField(default=0, db_index=True, verbose_name='Рейтинг')

    def __str__(self):
        return f'Вопрос #{self.id}'

    def get_absolute_url(self):
        return reverse("view_question", args=[self.id])

    class Meta:
        indexes = [
            GinIndex(  # GIN т.к. чтения кратно больше, чем записи
                name='trgm_idx_title',
                fields=['title'],
                opclasses=['gin_trgm_ops']
            ),
        ]

        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    objects = AnswerQuerySet.as_manager()  # гптшка с gemini'кой сказали, что эт best practices

    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='answers', verbose_name='Вопрос')
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='answers', verbose_name='Автор')
    answer_text = models.TextField(max_length=5000, verbose_name='Содержание ответа')
    answer_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата ответа')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def __str__(self):
        return (f'Ответ на #{self.question_id} '
                f'от #{self.author_id if self.author_id else 'Аноним'}')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class QuestionGrade(models.Model):
    CHOICES = (
        (-1, 'Dislike'),
        (1, 'Like')
    )

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Автор')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    grade = models.SmallIntegerField(choices=CHOICES, verbose_name='Оценка', default=0)

    def __str__(self):
        return (f'{'+1' if self.grade else '-1'} '
                f'для #{self.question_id}'
                f' от #{self.author_id if self.author_id else 'Анонима'}')

    class Meta:
        unique_together = ('author', 'question')

        verbose_name = 'Оценка вопроса'
        verbose_name_plural = 'Оценки вопросов'


class AnswerGrade(models.Model):
    CHOICES = (
        (-1, 'Dislike'),
        (1, 'Like')
    )

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Автор')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ')
    grade = models.SmallIntegerField(choices=CHOICES, verbose_name='Оценка', default=0)

    def __str__(self):
        return (f'{'+1' if self.grade > 0 else '-1'} для ответа'
                f' на #{self.answer_id}'
                f' от #{self.author_id if self.author_id else 'Анонима'}')

    class Meta:
        unique_together = ('author', 'answer')

        verbose_name = 'Оценка ответа'
        verbose_name_plural = 'Оценки ответов'
