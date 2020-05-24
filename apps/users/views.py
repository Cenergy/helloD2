

from django.views.generic.base import View
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend

from .models import UserProfile


# # custom_error404
# def page_not_found(request):
#     return render(request, '404.html')
#
#
# # custom_error500
# def page_error(request):
#     return render(request, '500.html')
#
#
# # custom_error403
# def permission_denied(request):
#     return render(request, '403.html')




class CustomBackend(ModelBackend):
    """
    custom authenticate
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(View):
    def get(self, request):
        return render(request, "users/index.html", locals())