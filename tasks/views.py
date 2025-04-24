import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .models import Task
from .serializers import TaskSerializer

# Get logger for tasks app
logger = logging.getLogger('tasks')

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        logger.info('Fetching list of all tasks')
        try:
            response = super().list(request, *args, **kwargs)
            logger.info(f'Successfully retrieved {self.get_queryset().count()} tasks')
            return response
        except Exception as e:
            logger.error(f'Error fetching tasks list: {str(e)}', exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        logger.info('Creating new task')
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f'Successfully created task: {response.data.get("title")} (ID: {response.data.get("id")})')
            return response
        except ValidationError as e:
            logger.warning(f'Validation error in task creation: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error creating task: {str(e)}', exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        logger.info(f'Updating task with ID: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
            logger.info(f'Current task data before update: {instance.__dict__}')
            response = super().update(request, *args, **kwargs)
            logger.info(f'Successfully updated task: {response.data.get("title")} (ID: {response.data.get("id")})')
            return response
        except ValidationError as e:
            logger.warning(f'Validation error in task update: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Error updating task: {str(e)}', exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'Deleting task with ID: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
            task_info = f'{instance.title} (ID: {instance.id})'
            response = super().destroy(request, *args, **kwargs)
            logger.info(f'Successfully deleted task: {task_info}')
            return response
        except Exception as e:
            logger.error(f'Error deleting task: {str(e)}', exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
