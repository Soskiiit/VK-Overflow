from django.shortcuts import HttpResponse


def index(request):
    return HttpResponse('meow')  # render(request, 'questions/index.html')
