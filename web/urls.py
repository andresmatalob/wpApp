from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('',views.home, name='web-home'),
    path('about/',views.about, name='web-about'),
    path('register/', views.registerPage, name='register_user'),
    path('login/', views.loginPage, name='login_user'),
    path('logout/', views.logoutPage, name='logout_user'),
    path('company/<int:company_id>/', views.company_detail, name='company_detail'),
    path('company/<int:company_id>/department/<int:department_id>/', views.department_detail, name='department_detail'),
    path('add_task/<int:project_id>/', views.add_task, name='add-task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete-task'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete-project'),
    path('delete_department/<int:department_id>/', views.delete_department, name='delete-department'),
    path('delete_company/<int:company_id>/', views.delete_company, name='delete-company'),
    path('create_project/<int:department_id>/', views.create_project, name='create-project'),
    path('create_department/<int:company_id>/', views.create_department, name='create-department'),
    path('department/<int:department_id>/add_users/', views.add_user_to_department, name='add_user_to_department'),
    path('company/<int:company_id>/add_user/', views.add_user_to_company, name='add_user_to_company'),
    path('create_company/', views.create_company, name='create_company'),
    path('modify_task/<int:task_id>/', views.modify_task, name='modify_task'),
]
