from django.contrib.auth.views import (
    LoginView,
    LogoutView
)
from django.urls import path

from .views import (
    SignUp,
    validate_username,
    validate_email,
)


app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),

    path('ajax/validate_username/', validate_username, name='validate_username'),
    path('ajax/validate_email/', validate_email, name='validate_email'),
]
