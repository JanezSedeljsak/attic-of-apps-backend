from .models import *
from .serializers import *

class HelperMethods:

    @staticmethod
    def addProgressToTask(task_id):
        task = Task.objects.get(pk=task_id)
        task_serializer = TaskSerializer(task)

        return task_serializer.data