from datetime import timedelta

from django.conf import settings
from django.core.cache import cache
from django.db.models import Count, Q
from django.tasks import task
from django.utils import timezone

from questions.models import Tag
from users.models import User


@task
def update_most_active_users():
    three_days_ago = timezone.now() - timedelta(days=3)
    most_active_users = User.objects.annotate(
        recent_answers_count=Count(
            'answers', filter=Q(answers__answer_date__gte=three_days_ago)
        )
    ).filter(recent_answers_count__gt=0).order_by('-recent_answers_count')[:5]
    cache.set('most_active_users', most_active_users, timeout=settings.CACHE_TTL)


@task
def update_popular_tags():
    tags_with_entries = Tag.objects.annotate(num_questions=Count('question'))
    popular_tags = tags_with_entries.order_by('-num_questions')[:5]
    cache.set('popular_tags', popular_tags, timeout=settings.CACHE_TTL)
