from django import forms
from django.core.exceptions import ValidationError

from .models import Answer, Question, Tag


class NewQuestionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mt-1', 'placeholder': 'Заголовок вашего вопроса'}
    ))
    question_text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control mt-1',
               'rows': '3',
               'placeholder': 'Подробно опишите свой вопрос'}
    ))
    tags = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mt-1', 'placeholder': 'Введите теги через запятую'}
    ), required=False)

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("author", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.author = self.author
        obj.save()  # Получаем ID ток при commit'e, а он нужен для вязки m2m связей
        tags = self.get_tags()
        for tag in tags:
            obj.tags.add(tag)
        obj.save()
        return obj

    def clean_tags(self):
        raw_line = self.cleaned_data.get('tags', '').strip()
        tags = list(map(str.capitalize, map(str.strip, raw_line.split(','))))
        if tags == ['']:
            return []
        for tag in tags:
            if len(tag) < 2:
                raise ValidationError(
                    'Тег не может быть короче 2 символов',
                    code='short_tag'
                )
        return tags

    def get_tags(self):
        for tag in self.cleaned_data['tags']:
            tag_obj, is_new = Tag.objects.get_or_create(name=tag)
            if is_new:
                tag_obj.save()
            yield tag_obj

    class Meta:
        model = Question
        fields = ['title', 'author', 'question_text', 'tags']


class NewAnswerForm(forms.ModelForm):
    answer_text = forms.CharField(widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("author", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        answer = super().save(commit=False)
        answer.author = self.author
        if commit:
            answer.save()
        return answer

    def clean_answer_text(self):
        line = self.cleaned_data['answer_text'].strip()
        if len(line) < 6:
            raise ValidationError(
                'Ответ не может быть короче 6 символов',
                code='short_answer'
            )
        return line

    class Meta:
        model = Answer
        fields = ['question', 'author', 'answer_text']
