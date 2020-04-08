from django.views.generic import View
from django.utils import timezone
from .render import Render
from msclone.tasks.models import Task


class Pdf(View):

    def get(self, request):
        tasks = Task.objects.all()
        today = timezone.now()
        params = {
            'today': today,
            'tasks': tasks,
            'user': (request.user.first_name + request.user.last_name) if request.user else '/',
            'smthn': 'kekec joža'
        }
        return Render.render('pdf.html', params)