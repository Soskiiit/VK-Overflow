from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, render

from core.utils import paginate
from questions.models import Answer, Question, Tag


questions = [
    {
        'qid': i,
        'author_id': i * 2,
        'title': f'Title {i + 1}',
        'description': 'some bla-bla-bla',
        'rating': hash(str(i)) % 23,  # pseudorandom positive number [0; 22]
        'tags': ['python', 'django'] if hash(str(i)) % 2 else ['golang', 'gRPC'],
    } for i in range(999999)
]

# Let's get tags sorted by popularity descending
tags = defaultdict(int)
for question in questions:
    for tag in question['tags']:
        tags[tag] += 1
tags = list(map(lambda x: x[0], sorted(tags.items(), key=lambda x: x[1], reverse=True)))

answers = [
    {
        'uid': i // 4,  # ~4 comms from 1 user
        'qid': hash(str(i)) % 99,
        'answer_rating': i,
        'text': 'bla-bla-bla',
    } for i in range(99)
]


def index(request):
    questions = Question.objects.all().order_by('-id')
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
    # Т.к. @property использовать для сортировки джанга не даст, то придётся поступать так
    question_list = Question.objects.annotate(
        rating_sort=Coalesce(Sum('questiongrade__grade'), 0)
    ).order_by('-rating_sort')

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
    question = get_object_or_404(Question, id=question_id)

    return render(
        request,
        'questions/question.html',
        {
            'question': question,
            'answers': Answer.objects.filter(question=question_id).order_by('-answer_date'),
        }
    )
