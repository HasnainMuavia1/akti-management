from django import template

register = template.Library()

@register.filter
def split_by_comma(value):
    """Split a comma-separated string into a list for iteration in templates."""
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(',') if item.strip()]
    return value

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key."""
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def lecture_key(lecture):
    """Create a unique key for a lecture using date and lecture number."""
    if lecture is None:
        return None
    return f"{lecture.date}_{lecture.lecture_number}"

@register.filter
def get_attendance_status(status_map, lecture):
    """Get attendance status for a specific lecture from the status map."""
    if not status_map or not lecture:
        return '-'
    
    key = f"{lecture.date}_{lecture.lecture_number}"
    return status_map.get(key, '-')
