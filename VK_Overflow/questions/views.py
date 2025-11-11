from collections import defaultdict

from django.shortcuts import render


questions = [
    {
        'qid': i,
        'author_id': i * 2,
        'title': f'Title {i + 1}',
        'description': 'some bla-bla-bla',
        'rating': hash(str(i)) % 23,  # pseudorandom positive number [0; 22]
        'tags': ['python', 'django'] if hash(str(i)) % 2 else ['golang', 'gRPC'],
    } for i in range(99)
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
    return render(
        request,
        'questions/index.html',
        {'questions': questions}
    )


def view_tag(request, tag):
    return render(
        request,
        'questions/index.html',
        {
            'questions': filter(lambda x: tag in x['tags'], questions),
            'page_title': f'Tag {tag}'
        }
    )


def my_questions(request):
    return render(
        request,
        'questions/questions-list.html',
        {'questions': questions, 'page_title': 'Мои вопросы'},
    )


def hot_questions(request):
    return render(
        request,
        'questions/questions-list.html',
        {
            'questions': sorted(questions, key=lambda x: -x['rating']),
            'page_title': 'Интереснейшие!! вопросы'
        }
    )


def new_question(request):
    return render(request, 'questions/new-question.html')


def view_question(request, question_id):
    return render(
        request,
        'questions/question.html',
        {
            'question': questions[question_id],
            'answers': filter(lambda x: x['qid'] == question_id, answers)
        }
    )
