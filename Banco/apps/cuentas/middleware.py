from django.shortcuts import redirect
from django.urls import reverse

class CompletarRegistroMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        authorized_paths = [reverse('completar_registro'), reverse('logout'), reverse('get_new_localidades')]
        if request.user.is_authenticated:
            if not request.user.has_privilege():
                if not request.user.profile_completed and request.path not in authorized_paths:
                    return redirect(reverse('completar_registro'))
        return self.get_response(request)