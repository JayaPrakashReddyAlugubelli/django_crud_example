from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employee-list'),
    path('create/', views.employee_create, name='employee-create'),
    path('update/<int:pk>/', views.employee_update, name='employee-update'),
    path('delete/<int:pk>/', views.employee_delete, name='employee-delete'),
]
