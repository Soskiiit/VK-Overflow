from django.db.models import Count

from questions.models import Tag


def popular_tags(request):
    tags_with_entries = Tag.objects.annotate(num_questions=Count('question'))
    popular_tags = tags_with_entries.order_by('-num_questions')[:5]
    return {'popular_tags': popular_tags}
