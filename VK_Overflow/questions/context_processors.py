from questions.views import tags


def popular_tags(request):
    return {'popular_tags': tags[:15]}
