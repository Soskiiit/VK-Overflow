from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from core.utils import paginate
from questions.models import Answer, Question, Tag


def index(request):
    questions = Question.objects.order_by('-id')
    page_obj = paginate(questions, request)

    return render(
        request,
        'questions/index.html',
        {'page_obj': page_obj}
    )


def view_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    question_list = Question.objects.filter(tags=tag).order_by('-creation_date')
    page_obj = paginate(question_list, request)

    return render(
        request,
        'questions/index.html',
        {
            'page_obj': page_obj,
            'page_title': f'Tag {tag}'
        }
    )


@login_required
def my_questions(request):
    question_list = Question.objects.filter(author=request.user).order_by('-creation_date')
    page_obj = paginate(question_list, request)

    return render(
        request,
        'questions/questions-list.html',
        {
            'page_obj': page_obj,
            'page_title': 'Мои вопросы'
        },
    )


def hot_questions(request):
    question_list = Question.objects.order_by('-rating')

    page_obj = paginate(question_list, request)
    return render(
        request,
        'questions/questions-list.html',
        {
            'page_obj': page_obj,
            'page_title': 'Интереснейшие!! вопросы'
        }
    )


def new_question(request):
    return render(request, 'questions/new-question.html')


def view_question(request, question_id):
    question = get_object_or_404(Question.objects.select_related('author'), id=question_id)
    answers = (Answer.objects.filter(question=question_id)
               .select_related('author').order_by('-answer_date'))

    return render(
        request,
        'questions/question.html',
        {
            'question': question,
            'answers': answers,
        }
    )
