# app/utils/filters.py
def apply_filters(query, model, filters):
    for field, value in filters.items():
        if hasattr(model, field):
            query = query.filter(getattr(model, field) == value)
    return query
