from math import ceil
from django.core.exceptions import ValidationError

def parse_pagination_params(query_params, default_page_size=20, max_page_size=100):
    try:
        page = int(query_params.get('page', 1))
        page_size = int(query_params.get('page_size', default_page_size))
    except (TypeError, ValueError):
        raise ValidationError('page and page_size must be integers.')
    if page < 1:
        raise ValidationError('page must be greater than or equal to 1.')
    if page_size < 1 or page_size > max_page_size:
        raise ValidationError(f'page_size must be between 1 and {max_page_size}.')
    return page, page_size

def paginate_records(records, page, page_size):
    total = len(records)
    start = (page - 1) * page_size
    return {
        'count': total,
        'page': page,
        'page_size': page_size,
        'total_pages': ceil(total / page_size) if total else 0,
        'results': records[start:start + page_size],
    }
