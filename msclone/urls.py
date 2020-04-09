from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from msclone.custom_auth.views import *
from msclone.tasks.views import *
from msclone.chat.views import *
from msclone.pdfgenerator.views import Pdf

urlpatterns = [

    # static admin view
    path('admin/', admin.site.urls),

    # hearbeat(test) route
    path('heartbeat', heartbeat),

    # auth routes
    path('auth/login', login),
    path('auth/logout', logout),
    path('auth/create_auth', create_auth),
    path('auth/get_user', get_user),

    # task routes
    path('task/<int:task_id>', get_task),
    path('task/create', create_task),
    path('task/<int:task_id>/<int:subtask_id>', get_sub_task),
    path('tasks', get_all_tasks),
    path('task-units', get_all_units),
    path('task-statuses', get_all_statuses),
    path('your-tasks/range/<slug:start_date>/<slug:end_date>', get_your_tasks_for_daterange),

    # chat routes
    path('chat/send_message', send_message),
    path('message/<int:message_id>', update_message),
    path('messages/<int:chat_id>', get_all_messages),

    # generate pdf route
    path('render/pdf/', Pdf.as_view())
]
