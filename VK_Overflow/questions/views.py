import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.utils import paginate
from questions.models import Answer, AnswerGrade, Question, QuestionGrade, Tag
from questions.forms import NewAnswerForm, NewQuestionForm
from questions.utils import get_centrifugo_token


def index(request):
    questions = Question.objects.with_votes_from(request.user).order_by('-id')
    page_obj = paginate(questions, request)

    return render(
        request,
        'questions/index.html',
        {'page_obj': page_obj}
    )


def view_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
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
            question = form.save()
            return redirect('view_question', question_id=question.id)
    return render(request, 'questions/new-question.html', {'form': form})


def view_question(request, question_id):
    question = get_object_or_404(Question.objects.select_related('author')
                                 .with_votes_from(request.user), id=question_id)
    answers = (Answer.objects.filter(question=question_id).with_votes_from(request.user)
               .select_related('author').order_by('answer_date'))

    return render(
        request,
        'questions/question.html',
        {
            'question':
                question,
            'answers':
                answers,
            'centrifugo_ws_url':
                settings.CENTRIFUGO_WS_URL,
            'centrifugo_token':
                get_centrifugo_token(request.user.id) if request.user.is_authenticated else '',
        }
    )


# AJAX handlers


@login_required
@require_POST
def new_answer(request):
    form = NewAnswerForm(request.POST, author=request.user)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': form.errors}, status=400)


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


@login_required
@require_POST
def set_best_answer(request):
    data = json.loads(request.body.decode('utf-8'))

    if request.user.id != data['author']:
        return JsonResponse({'error': 'Only author can set best answer'}, status=400)

    try:
        question = Question.objects.get(id=data['question_id'])
    except Question.DoesNotExist:
        return JsonResponse({'error': 'Question doesn\'t exist'}, status=404)

    try:
        answer = Answer.objects.get(id=data['answer_id'])
    except Answer.DoesNotExist:
        return JsonResponse({'error': 'Answer doesn\'t exist'}, status=404)

    question.best_answer = answer
    question.save()
    return JsonResponse({'status': 'ok'})


def search_suggestions(request):
    query = request.GET.get('q', '').strip()

    if len(query) < 3:
        return JsonResponse({'results': []})

    vector = SearchVector('title', weight='A') + SearchVector('question_text', weight='B')
    search_query = SearchQuery(query)
    questions = Question.objects.annotate(
        rank=SearchRank(vector, search_query)
    ).filter(rank__gte=0.4).order_by('-rating', '-rank')[:5]

    if not questions:
        questions = Question.objects.annotate(
            similarity=TrigramSimilarity('title', query)
        ).filter(similarity__gte=0.2).order_by('-similarity', '-rating')[:5]

    results = [
        {
            'id': q.id,
            'title': q.title,
            'url': q.get_absolute_url(),
            'likes': q.rating
        } for q in questions
    ]

    return JsonResponse({'results': results})
