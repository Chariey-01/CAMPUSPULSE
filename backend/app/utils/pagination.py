from flask import request


def paginate_query(query, serializer=None, default_per_page=10, max_per_page=50):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", default_per_page, type=int)
    per_page = min(per_page, max_per_page)  # caller can't request more than max_per_page

    # error_out=False -> an out-of-range page returns an empty `items` list
    # instead of raising a 404, which keeps pagination lenient at the API boundary
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    if serializer:
        items = serializer(pagination.items)
    else:
        items = [item.to_dict() for item in pagination.items]

    return {
        "items": items,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "total_pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
    }
