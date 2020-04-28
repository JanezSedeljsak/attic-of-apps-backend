from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from core.custom_auth.views import *
from core.tasks.views import *
from core.chat.views import *
from core.pickers.views import *
from core.pdfgenerator.views import *

urlpatterns = [

    # static admin view
    path('admin/', admin.site.urls),

    # hearbeat(test) route
    path('heartbeat', heartbeat),

    # auth routes
    path('auth/login', login),
    path('auth/google', google_auth),
    path('auth/logout', logout),
    path('auth/create', create_auth),
    path('auth/update', update_auth),
    path('auth/econfirm', email_confirm),
    path('auth/send-reset', send_reset),
    path('auth/pass-reset', reset_password),

    # task routes
    path('task/<int:task_id>', get_task),
    path('task/detail/<int:task_id>', get_task_detail),
    path('task/create', create_task),
    path('tasks', get_all_tasks),
    path('tasks/range', get_your_tasks_for_daterange),

    # chat routes
    path('chat/send_message', send_message),
    path('message/<int:message_id>', update_message),
    path('messages/<int:chat_id>', get_all_messages),

    # picker routes
    path('picker/user', collaborator_picker),
    path('picker/status', status_picker),
    path('picker/permission', permission_picker),

    # generate pdf route
    path('render/pdf/weekly', weekly_pdf),
    path('render/pdf/task', task_pdf)
]
