from django.contrib import admin

from questions.models import Answer, AnswerGrade, Question, QuestionGrade, Tag


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    fields = ('question', 'author', 'answer_text', 'answer_date')
    readonly_fields = ('answer_date',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ('title', 'author', 'tags', 'question_text', 'creation_date')
    readonly_fields = ('creation_date',)
    list_display = ('title', 'author')


admin.site.register(Tag)
admin.site.register(AnswerGrade)
admin.site.register(QuestionGrade)
