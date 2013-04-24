def login_as_shorter_username(request, user):
    return len(user.username) < len(request.user.username)
