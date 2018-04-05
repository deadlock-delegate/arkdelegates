def has_edit_permissions(user):
    is_editor = user.groups.filter(name='editor').exists()
    return (is_editor or user.is_superuser)
