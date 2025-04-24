import pytest
from django.urls import reverse
from tasks.models import Task

@pytest.mark.django_db
class TestTaskViews:
    def test_task_list_view(self, client):
        # Create some test tasks
        Task.objects.create(title="Test Task 1", description="Description 1")
        Task.objects.create(title="Test Task 2", description="Description 2")
        
        # Get the response from the view
        url = reverse('task-list')
        response = client.get(url)
        
        # Assert response status code and context
        assert response.status_code == 200
        assert len(response.context['tasks']) == 2
        assert 'Test Task 1' in str(response.content)
        assert 'Test Task 2' in str(response.content)

    def test_task_create_view(self, client):
        # Test GET request
        url = reverse('task-create')
        response = client.get(url)
        assert response.status_code == 200
        
        # Test POST request
        data = {
            'title': 'New Task',
            'description': 'New Description'
        }
        response = client.post(url, data)
        
        # Assert redirect and task creation
        assert response.status_code == 302
        assert Task.objects.count() == 1
        task = Task.objects.first()
        assert task.title == 'New Task'
        assert task.description == 'New Description'

    def test_task_update_view(self, client):
        # Create a test task
        task = Task.objects.create(
            title="Original Title",
            description="Original Description"
        )
        
        # Test GET request
        url = reverse('task-update', args=[task.pk])
        response = client.get(url)
        assert response.status_code == 200
        assert 'Original Title' in str(response.content)
        
        # Test POST request
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'completed': 'on'
        }
        response = client.post(url, data)
        
        # Assert redirect and task update
        assert response.status_code == 302
        task.refresh_from_db()
        assert task.title == 'Updated Title'
        assert task.description == 'Updated Description'
        assert task.completed == True

    def test_task_delete_view(self, client):
        # Create a test task
        task = Task.objects.create(
            title="Task to Delete",
            description="This task will be deleted"
        )
        
        # Test GET request (confirmation page)
        url = reverse('task-delete', args=[task.pk])
        response = client.get(url)
        assert response.status_code == 200
        assert 'Task to Delete' in str(response.content)
        
        # Test POST request (actual deletion)
        response = client.post(url)
        
        # Assert redirect and task deletion
        assert response.status_code == 302
        assert Task.objects.count() == 0

    def test_task_not_found(self, client):
        # Test accessing non-existent task
        url = reverse('task-update', args=[999])
        response = client.get(url)
        assert response.status_code == 404

        url = reverse('task-delete', args=[999])
        response = client.get(url)
        assert response.status_code == 404
