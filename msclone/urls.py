from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from msclone.custom_auth.views import *
from msclone.tasks.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login', login),
    path('auth/logout', logout),
    path('auth/create_auth', create_auth),
    path('auth/get_user', get_user),
    path('heartbeat', heartbeat)
]
