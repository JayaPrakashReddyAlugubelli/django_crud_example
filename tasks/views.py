from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Task
from django.contrib import messages

# Create your views here.

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']

def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Task.objects.create(title=title, description=description)
        messages.success(request, 'Task created successfully!')
        return redirect('task-list')
    return render(request, 'tasks/task_form.html')

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.completed = 'completed' in request.POST
        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('task-list')
    return render(request, 'tasks/task_form.html', {'task': task})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task-list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
