from django.core.cache import cache

from .tasks import update_most_active_users, update_popular_tags


def get_popular_tags(request):
    popular_tags = cache.get('popular_tags')

    if popular_tags is not None:
        return {'popular_tags': popular_tags}

    update_popular_tags.enqueue()
    popular_tags = cache.get('popular_tags')

    return {'popular_tags': popular_tags}


def get_most_active_users(request):
    most_active_users = cache.get('most_active_users')

    if most_active_users is not None:
        return {'most_active_users': most_active_users}

    update_most_active_users.enqueue()
    most_active_users = cache.get('most_active_users')

    return {'most_active_users': most_active_users}
