import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Employee
from datetime import datetime

# Get logger for employees app
logger = logging.getLogger('employees')

# Create your views here.

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    ordering = ['-date_of_joining']

    def get(self, request, *args, **kwargs):
        logger.info('Fetching list of all employees')
        try:
            response = super().get(request, *args, **kwargs)
            logger.info(f'Successfully retrieved {self.get_queryset().count()} employees')
            return response
        except Exception as e:
            logger.error(f'Error fetching employees list: {str(e)}', exc_info=True)
            raise

def validate_employee_data(data):
    errors = {}
    required_fields = ['full_name', 'date_of_birth', 'gender', 'phone_number', 
                      'email', 'address', 'job_title', 'department', 
                      'date_of_joining', 'work_location']
    
    # Check required fields
    for field in required_fields:
        if not data.get(field):
            errors[field] = 'This field is required.'
    
    # Validate email format
    email = data.get('email')
    if email:
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = 'Enter a valid email address.'
    
    # Validate phone number format (basic validation)
    phone = data.get('phone_number')
    if phone and not (phone.startswith('+') and len(phone) >= 10):
        errors['phone_number'] = 'Enter a valid phone number starting with + and at least 10 digits.'
    
    return errors

def employee_create(request):
    logger.info('Accessing employee creation form')
    if request.method == 'POST':
        try:
            logger.info('Processing employee creation request')
            errors = validate_employee_data(request.POST)
            if errors:
                logger.warning(f'Validation errors in employee creation: {errors}')
                return render(request, 'employees/employee_form.html', {'errors': errors})

            employee = Employee(
                full_name=request.POST.get('full_name'),
                date_of_birth=datetime.strptime(request.POST.get('date_of_birth'), '%Y-%m-%d'),
                gender=request.POST.get('gender'),
                phone_number=request.POST.get('phone_number'),
                email=request.POST.get('email'),
                address=request.POST.get('address'),
                job_title=request.POST.get('job_title'),
                department=request.POST.get('department'),
                employee_id=request.POST.get('employee_id'),
                date_of_joining=datetime.strptime(request.POST.get('date_of_joining'), '%Y-%m-%d'),
                work_location=request.POST.get('work_location')
            )
            employee.save()
            logger.info(f'Successfully created employee: {employee.full_name} (ID: {employee.employee_id})')
            messages.success(request, 'Employee registered successfully!')
            return redirect('employee-list')
        except Exception as e:
            logger.error(f'Error creating employee: {str(e)}', exc_info=True)
            messages.error(request, f'Error creating employee: {str(e)}')
            return render(request, 'employees/employee_form.html')
    return render(request, 'employees/employee_form.html')

def employee_update(request, pk):
    logger.info(f'Accessing employee update form for ID: {pk}')
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        try:
            logger.info(f'Processing update request for employee ID: {pk}')
            errors = validate_employee_data(request.POST)
            if errors:
                logger.warning(f'Validation errors in employee update: {errors}')
                return render(request, 'employees/employee_form.html', 
                            {'employee': employee, 'errors': errors})

            # Log old values before update
            logger.info(f'Current employee data before update: {employee.__dict__}')

            employee.full_name = request.POST.get('full_name')
            employee.date_of_birth = datetime.strptime(request.POST.get('date_of_birth'), '%Y-%m-%d')
            employee.gender = request.POST.get('gender')
            employee.phone_number = request.POST.get('phone_number')
            employee.email = request.POST.get('email')
            employee.address = request.POST.get('address')
            employee.job_title = request.POST.get('job_title')
            employee.department = request.POST.get('department')
            employee.employee_id = request.POST.get('employee_id')
            employee.date_of_joining = datetime.strptime(request.POST.get('date_of_joining'), '%Y-%m-%d')
            employee.work_location = request.POST.get('work_location')
            employee.save()

            logger.info(f'Successfully updated employee: {employee.full_name} (ID: {employee.employee_id})')
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee-list')
        except Exception as e:
            logger.error(f'Error updating employee {pk}: {str(e)}', exc_info=True)
            messages.error(request, f'Error updating employee: {str(e)}')
            return render(request, 'employees/employee_form.html', {'employee': employee})
    return render(request, 'employees/employee_form.html', {'employee': employee})

def employee_delete(request, pk):
    logger.info(f'Accessing employee delete confirmation for ID: {pk}')
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        try:
            employee_info = f'{employee.full_name} (ID: {employee.employee_id})'
            employee.delete()
            logger.info(f'Successfully deleted employee: {employee_info}')
            messages.success(request, 'Employee deleted successfully!')
            return redirect('employee-list')
        except Exception as e:
            logger.error(f'Error deleting employee {pk}: {str(e)}', exc_info=True)
            messages.error(request, f'Error deleting employee: {str(e)}')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})
