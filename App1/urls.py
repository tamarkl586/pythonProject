from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # ==================== AUTHENTICATION ====================
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # ==================== PROFILE ====================
    path('profile/setup/', views.profile_setup, name='profile_setup'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile_detail, name='profile_detail'),
    
    # ==================== HOME PAGE ====================
    path('', views.home, name='home'),
    
    # ==================== TASKS ====================
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:id>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:id>/status/', views.update_task_status, name='update_task_status'),
    path('tasks/<int:id>/associate/', views.associate_task, name='associate_task'),
    path('tasks/<int:id>/delete/', views.delete_task, name='delete_task'),
]
