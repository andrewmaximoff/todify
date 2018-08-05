from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import PersonCreationForm
from .models import Person


class SignUp(CreateView):
    form_class = PersonCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = reverse_lazy('home')
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)


def validate_username(request):
    username = request.GET.get('username', None)
    if username is not None:
        username = username.lowercase()
    data = {
        'is_taken': Person.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)


def validate_email(request):
    username = request.GET.get('email', None)
    data = {
        'is_taken': Person.objects.filter(email__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this email already exists.'
    return JsonResponse(data)
