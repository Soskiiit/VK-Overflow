import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse

from core.utils import paginate
from questions.models import Answer, AnswerGrade, Question, QuestionGrade, Tag
from questions.forms import NewQuestionForm


def index(request):
    questions = Question.objects.with_votes_from(request.user).order_by('-id')
    page_obj = paginate(questions, request)

    return render(
        request,
        'questions/index.html',
        {'page_obj': page_obj}
    )


def view_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    question_list = (Question.objects.filter(tags=tag)
                     .with_votes_from(request.user).order_by('-creation_date'))
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
    question_list = (Question.objects.filter(author=request.user)
                     .with_votes_from(request.user).order_by('-creation_date'))
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
    question_list = Question.objects.with_votes_from(request.user).order_by('-rating')

    page_obj = paginate(question_list, request)
    return render(
        request,
        'questions/questions-list.html',
        {
            'page_obj': page_obj,
            'page_title': 'Интереснейшие!! вопросы'
        }
    )


@login_required
def new_question(request):
    form = NewQuestionForm()
    if request.method == 'POST':
        form = NewQuestionForm(request.POST, author=request.user)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    return render(request, 'questions/new-question.html', {'form': form})


def view_question(request, question_id):
    question = get_object_or_404(Question.objects.select_related('author')
                                 .with_votes_from(request.user), id=question_id)
    answers = (Answer.objects.filter(question=question_id).with_votes_from(request.user)
               .select_related('author').order_by('-answer_date'))

    return render(
        request,
        'questions/question.html',
        {
            'question': question,
            'answers': answers,
        }
    )

# AJAX handlers


@login_required
@require_POST
def vote(request):
    data = json.loads(request.body.decode('utf-8'))
    if data.get('question_id'):
        question_id = data['question_id']
        vote, created = QuestionGrade.objects.get_or_create(
            question_id=question_id, author=request.user
        )
    else:
        answer_id = data['answer_id']
        vote, created = AnswerGrade.objects.get_or_create(answer_id=answer_id, author=request.user)

    action = data['action']
    if action == 'like':
        if vote.grade == 1:
            vote.grade = 0
        else:
            vote.grade = 1
    else:
        if vote.grade == -1:
            vote.grade = 0
        else:
            vote.grade = -1
    vote.save()
    return JsonResponse({'user_vote': vote.grade})
