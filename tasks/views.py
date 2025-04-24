import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib import messages
from .models import Task

# Get logger for tasks app
logger = logging.getLogger('tasks')

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']

    def get(self, request, *args, **kwargs):
        logger.info('Fetching list of all tasks')
        try:
            response = super().get(request, *args, **kwargs)
            logger.info(f'Successfully retrieved {self.get_queryset().count()} tasks')
            return response
        except Exception as e:
            logger.error(f'Error fetching tasks list: {str(e)}', exc_info=True)
            raise

def task_create(request):
    logger.info('Accessing task creation form')
    if request.method == 'POST':
        try:
            logger.info('Processing task creation request')
            title = request.POST.get('title')
            description = request.POST.get('description')

            if not title:
                logger.warning('Task creation failed: Title is required')
                messages.error(request, 'Title is required')
                return render(request, 'tasks/task_form.html')

            task = Task.objects.create(
                title=title,
                description=description
            )
            logger.info(f'Successfully created task: {task.title} (ID: {task.id})')
            messages.success(request, 'Task created successfully!')
            return redirect('task-list')
        except Exception as e:
            logger.error(f'Error creating task: {str(e)}', exc_info=True)
            messages.error(request, f'Error creating task: {str(e)}')
            return render(request, 'tasks/task_form.html')
    return render(request, 'tasks/task_form.html')

def task_update(request, pk):
    logger.info(f'Accessing task update form for ID: {pk}')
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        try:
            logger.info(f'Processing update request for task ID: {pk}')
            title = request.POST.get('title')
            description = request.POST.get('description')

            if not title:
                logger.warning('Task update failed: Title is required')
                messages.error(request, 'Title is required')
                return render(request, 'tasks/task_form.html', {'task': task})

            # Log old values before update
            logger.info(f'Current task data before update: {task.__dict__}')

            task.title = title
            task.description = request.POST.get('description')
            task.completed = 'completed' in request.POST
            task.save()

            logger.info(f'Successfully updated task: {task.title} (ID: {task.id})')
            messages.success(request, 'Task updated successfully!')
            return redirect('task-list')
        except Exception as e:
            logger.error(f'Error updating task {pk}: {str(e)}', exc_info=True)
            messages.error(request, f'Error updating task: {str(e)}')
            return render(request, 'tasks/task_form.html', {'task': task})
    return render(request, 'tasks/task_form.html', {'task': task})

def task_delete(request, pk):
    logger.info(f'Accessing task delete confirmation for ID: {pk}')
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        try:
            task_info = f'{task.title} (ID: {task.id})'
            task.delete()
            logger.info(f'Successfully deleted task: {task_info}')
            messages.success(request, 'Task deleted successfully!')
            return redirect('task-list')
        except Exception as e:
            logger.error(f'Error deleting task {pk}: {str(e)}', exc_info=True)
            messages.error(request, f'Error deleting task: {str(e)}')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
