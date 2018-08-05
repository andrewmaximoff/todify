from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, include

from todo.views import task_list


urlpatterns = [
    path('', task_list, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('todo/', include('todo.urls')),
]

urlpatterns += staticfiles_urlpatterns()
