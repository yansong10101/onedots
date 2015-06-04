__author__ = 'zys'


def update_session_timeout(request):
    if request.user.is_authenticated():
        request.session.set_expiry(300)
