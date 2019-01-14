from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, include

from todify.todo.views import task_list


urlpatterns = [
    path('', task_list, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('todify.accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('todo/', include('todify.todo.urls')),
]

urlpatterns += staticfiles_urlpatterns()
