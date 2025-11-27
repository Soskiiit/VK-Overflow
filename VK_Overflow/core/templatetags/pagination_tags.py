from django import template

register = template.Library()


@register.simple_tag
def get_optimized_page_range(page_obj, pages_around=2):
    current_page = page_obj.number
    total_pages = page_obj.paginator.num_pages

    start_page = max(1, current_page - pages_around)
    end_page = min(total_pages, current_page + pages_around)

    return range(start_page, end_page + 1)
