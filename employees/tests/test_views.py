import pytest
from django.urls import reverse
from employees.models import Employee
from datetime import date

@pytest.mark.django_db
class TestEmployeeViews:
    @pytest.fixture
    def sample_employee_data(self):
        return {
            'full_name': 'John Doe',
            'date_of_birth': '1990-01-01',
            'gender': 'M',
            'phone_number': '+1234567890',
            'email': 'john.doe@example.com',
            'address': '123 Main St, City',
            'job_title': 'Software Engineer',
            'department': 'Engineering',
            'employee_id': 'EMP001',
            'date_of_joining': '2023-01-01',
            'work_location': 'New York'
        }

    @pytest.fixture
    def create_employee(self, sample_employee_data):
        return Employee.objects.create(
            full_name=sample_employee_data['full_name'],
            date_of_birth=date.fromisoformat(sample_employee_data['date_of_birth']),
            gender=sample_employee_data['gender'],
            phone_number=sample_employee_data['phone_number'],
            email=sample_employee_data['email'],
            address=sample_employee_data['address'],
            job_title=sample_employee_data['job_title'],
            department=sample_employee_data['department'],
            employee_id=sample_employee_data['employee_id'],
            date_of_joining=date.fromisoformat(sample_employee_data['date_of_joining']),
            work_location=sample_employee_data['work_location']
        )

    def test_employee_list_view(self, client, create_employee):
        # Test empty list
        url = reverse('employee-list')
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.context['employees']) == 1
        assert 'John Doe' in str(response.content)
        assert 'EMP001' in str(response.content)

    def test_employee_create_view(self, client, sample_employee_data):
        # Test GET request
        url = reverse('employee-create')
        response = client.get(url)
        assert response.status_code == 200
        assert 'Register New Employee' in str(response.content)

        # Test POST request with valid data
        response = client.post(url, sample_employee_data)
        assert response.status_code == 302  # Redirect after success
        assert Employee.objects.count() == 1
        employee = Employee.objects.first()
        assert employee.full_name == 'John Doe'
        assert employee.employee_id == 'EMP001'

        # Test POST request with invalid data
        invalid_data = sample_employee_data.copy()
        invalid_data['email'] = 'invalid-email'  # Invalid email format
        response = client.post(url, invalid_data)
        assert response.status_code == 200  # Returns to form
        assert 'Enter a valid email address' in str(response.content)

    def test_employee_update_view(self, client, create_employee, sample_employee_data):
        # Test GET request
        url = reverse('employee-update', args=[create_employee.pk])
        response = client.get(url)
        assert response.status_code == 200
        assert 'Edit Employee' in str(response.content)
        assert 'John Doe' in str(response.content)

        # Test POST request with valid data
        updated_data = sample_employee_data.copy()
        updated_data['full_name'] = 'Jane Doe'
        updated_data['job_title'] = 'Senior Engineer'
        response = client.post(url, updated_data)
        assert response.status_code == 302  # Redirect after success
        
        employee = Employee.objects.get(pk=create_employee.pk)
        assert employee.full_name == 'Jane Doe'
        assert employee.job_title == 'Senior Engineer'

        # Test POST request with missing required field
        invalid_data = sample_employee_data.copy()
        invalid_data.pop('full_name')  # Remove required field
        response = client.post(url, invalid_data)
        assert response.status_code == 200  # Returns to form with errors
        assert 'This field is required' in str(response.content)

        # Test POST request with invalid email
        invalid_data = sample_employee_data.copy()
        invalid_data['email'] = 'invalid-email'
        response = client.post(url, invalid_data)
        assert response.status_code == 200  # Returns to form with errors
        assert 'Enter a valid email address' in str(response.content)
        employee.refresh_from_db()
        assert employee.email == sample_employee_data['email']  # Email should not be updated

    def test_employee_delete_view(self, client, create_employee):
        # Test GET request (confirmation page)
        url = reverse('employee-delete', args=[create_employee.pk])
        response = client.get(url)
        assert response.status_code == 200
        assert 'Are you sure you want to delete' in str(response.content)
        assert 'John Doe' in str(response.content)

        # Test POST request (actual deletion)
        response = client.post(url)
        assert response.status_code == 302  # Redirect after success
        assert Employee.objects.count() == 0

    def test_employee_not_found(self, client):
        # Test accessing non-existent employee
        url = reverse('employee-update', args=[999])
        response = client.get(url)
        assert response.status_code == 404

        url = reverse('employee-delete', args=[999])
        response = client.get(url)
        assert response.status_code == 404

    def test_unique_constraints(self, client, create_employee, sample_employee_data):
        # Test creating employee with duplicate email
        url = reverse('employee-create')
        response = client.post(url, sample_employee_data)
        assert response.status_code == 200  # Returns to form
        assert 'Error creating employee' in str(response.content)

        # Test creating employee with duplicate employee_id
        new_data = sample_employee_data.copy()
        new_data['email'] = 'different.email@example.com'
        response = client.post(url, new_data)
        assert response.status_code == 200
        assert 'Error creating employee' in str(response.content)
