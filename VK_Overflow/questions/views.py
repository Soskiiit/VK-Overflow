from django.shortcuts import render


def index(request):
    return render(request, 'questions/index.html')


def my_questions(request):
    return render(request, 'questions/my-questions.html')


def new_question(request):
    return render(request, 'questions/new-question.html')
