import json

from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views import View
from django.views.decorators.http import require_POST

from core.utils import paginate
from questions.models import Answer, AnswerGrade, Question, QuestionGrade, Tag
from questions.forms import NewAnswerForm, NewQuestionForm


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
            'question': question,
            'answers': answers,
        }
    )


# AJAX handlers


@login_required
@require_POST
def new_answer(request):
    form = NewAnswerForm(request.POST, author=request.user)
    if form.is_valid():
        answer = form.save()
        html = render_to_string('questions/answer_card.html', {'ans': answer}, request=request)
        return JsonResponse({'html': html, 'id': answer.id})
    return JsonResponse({'error': form.errors}, status=400)


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


class VoteQuestionView(View):
    http_method_names = ['post']

    def get_question_grade(self, question_id):
        try:
            vote, is_created = QuestionGrade.objects.get_or_create(
                question_id=question_id, author=self.request.user)
            return vote, is_created
        except IntegrityError:
            vote = QuestionGrade.objects.filter(
                question_id=question_id, author=self.request.user).first()
            return vote, False

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)

        question_id = kwargs['question_id']

        question = Question.objects.filter(id=question_id).first()
        if question is None:
            return JsonResponse(
                {'error': f'Question with Id="{question_id}" not found'}, status=404)

        try:
            data = json.loads(request.body)
            action = data.get('action')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if action not in ['like', 'dislike']:
            return JsonResponse({'error': f'Unknown action="{action}"'}, status=400)

        vote, _ = self.get_question_grade(question.pk)
        if action == 'like':
            vote.grade = 0 if vote.grade == 1 else 1
        elif action == 'dislike':
            vote.grade = 0 if vote.grade == -1 else -1

        vote.save(update_fields=['grade'])
        return JsonResponse({'user_vote': vote.grade}, status=200)


class VoteAnswerView(View):
    http_method_names = ['post']

    def get_answer_grade(self, answer_id):
        try:
            vote, is_created = AnswerGrade.objects.get_or_create(
                answer_id=answer_id, author=self.request.user)
            return vote, is_created
        except IntegrityError:
            vote = AnswerGrade.objects.filter(
                answer_id=answer_id, author=self.request.user).first()
            return vote, False

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)

        answer_id = kwargs['answer_id']

        answer = Answer.objects.filter(id=answer_id).first()
        if answer is None:
            return JsonResponse(
                {'error': f'Answer with Id="{answer_id}" not found'}, status=404)

        try:
            data = json.loads(request.body)
            action = data.get('action')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if action not in ['like', 'dislike']:
            return JsonResponse({'error': f'Unknown action="{action}"'}, status=400)

        vote, _ = self.get_answer_grade(answer.pk)
        if action == 'like':
            vote.grade = 0 if vote.grade == 1 else 1
        elif action == 'dislike':
            vote.grade = 0 if vote.grade == -1 else -1

        vote.save(update_fields=['grade'])
        return JsonResponse({'user_vote': vote.grade}, status=200)


class SetBestAnswerView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)

        try:
            question = Question.objects.get(id=data['question_id'])

            if request.user.id != question.author.id:
                return JsonResponse({'error': 'Only author can set best answer'}, status=403)
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question doesn\'t exist'}, status=404)

        try:
            answer = Answer.objects.get(id=data['answer_id'])
        except Answer.DoesNotExist:
            return JsonResponse({'error': 'Answer doesn\'t exist'}, status=404)

        question.best_answer = answer
        question.save()
        return JsonResponse({'status': 'ok'})
