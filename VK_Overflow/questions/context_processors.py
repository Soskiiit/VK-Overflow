from datetime import timedelta

from django.core.cache import cache
from django.db.models import Count, Q
from django.utils import timezone

from questions.models import Tag
from users.models import User


def get_popular_tags(request):
    popular_tags = cache.get('popular_tags')

    if popular_tags is not None:
        return {'popular_tags': popular_tags}

    tags_with_entries = Tag.objects.annotate(num_questions=Count('question'))
    popular_tags = tags_with_entries.order_by('-num_questions')[:5]
    cache.set('popular_tags', popular_tags, timeout=30 * 60)

    return {'popular_tags': popular_tags}


def get_most_active_users(request):
    most_active_users = cache.get('most_active_users')

    if most_active_users is not None:
        return {'most_active_users': most_active_users}

    three_days_ago = timezone.now() - timedelta(days=3)
    most_active_users = User.objects.annotate(
        recent_answers_count=Count(
            'answers', filter=Q(answers__answer_date__gte=three_days_ago)
        )
    ).filter(recent_answers_count__gt=0).order_by('-recent_answers_count')[:5]
    cache.set('most_active_users', most_active_users, timeout=30 * 60)

    return {'most_active_users': most_active_users}
