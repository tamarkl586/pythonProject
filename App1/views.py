from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_http_methods
from .models import Task, CustomUser, Team
from .forms import SignUpForm, ProfileSetupForm, TaskForm, TaskStatusUpdateForm


# ==================== REGISTRATION ====================
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_setup')
    else:
        form = SignUpForm()
    
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


# ==================== LOGIN ====================
@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # If user hasn't set up profile yet, redirect to profile setup
                if not user.team:
                    return redirect('profile_setup')
                # If profile is complete, redirect to task list
                return redirect('task_list')
    else:
        form = AuthenticationForm()
    
    # Add Bootstrap styling to form fields
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    
    context = {'form': form}
    return render(request, 'registration/login.html', context)


# ==================== LOGOUT ====================
@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('home')


# ==================== PROFILE SETUP (After first login) ====================
@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def profile_setup(request):
    user = request.user
    
    if request.method == "POST":
        form = ProfileSetupForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = ProfileSetupForm(instance=user)
    
    context = {'form': form, 'user': user}
    return render(request, 'registration/profile_setup.html', context)


# ==================== EDIT PROFILE ====================
@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def edit_profile(request):
    user = request.user
    
    if request.method == "POST":
        form = ProfileSetupForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileSetupForm(instance=user)
    
    context = {'form': form, 'user': user}
    return render(request, 'profile/edit_profile.html', context)


# ==================== VIEW PROFILE ====================
@login_required(login_url='login')
def profile_detail(request):
    user = request.user
    context = {
        'user': user,
        'team': user.team,
        'role': user.role,
    }
    return render(request, 'profile/profile_detail.html', context)


# ==================== HOME PAGE ====================
def home(request):
    if request.user.is_authenticated:
        user = request.user
        team = user.team
        
        if team:
            all_tasks = Task.objects.filter(team=team).order_by('due_date')
            assigned_tasks = all_tasks.filter(assigned_to=user)
            task_stats = {
                'total': all_tasks.count(),
                'new': all_tasks.filter(status='New').count(),
                'in_progress': all_tasks.filter(status='In Progress').count(),
                'completed': all_tasks.filter(status='Completed').count(),
            }
        else:
            all_tasks = Task.objects.none()
            assigned_tasks = Task.objects.none()
            task_stats = {'total': 0, 'new': 0, 'in_progress': 0, 'completed': 0}
        
        context = {
            'user': user,
            'team': team,
            'recent_tasks': all_tasks[:5],
            'assigned_tasks': assigned_tasks,
            'task_stats': task_stats,
        }
        return render(request, 'home.html', context)
    
    return render(request, 'home.html')


# ==================== TASK LIST (Filtered by team and status) ====================
@login_required(login_url='login')
def task_list(request):
    user = request.user
    team = user.team
    
    if not team:
        return redirect('profile_setup')
    
    tasks = Task.objects.filter(team=team).order_by('due_date')
    
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    task_summary = {
        'total': tasks.count(),
        'new': tasks.filter(status='New').count(),
        'in_progress': tasks.filter(status='In Progress').count(),
        'completed': tasks.filter(status='Completed').count(),
    }
    
    context = {
        'tasks': tasks,
        'team': team,
        'user': user,
        'current_status_filter': status_filter,
        'task_summary': task_summary,
    }
    return render(request, 'tasks/task_list.html', context)


# ==================== TASK DETAIL ====================
@login_required(login_url='login')
def task_detail(request, id):
    task = get_object_or_404(Task, pk=id)
    user = request.user
    
    if task.team != user.team:
        return redirect('task_list')
    
    is_assigned = task.assigned_to == user
    is_manager = user.role == 'Manager'
    
    context = {
        'task': task,
        'is_assigned': is_assigned,
        'is_manager': is_manager,
    }
    return render(request, 'tasks/task_detail.html', context)


# ==================== CREATE TASK (Manager only) ====================
@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def create_task(request):
    user = request.user
    
    if user.role != 'Manager':
        return redirect('task_list')
    
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.team = user.team
            task.status = 'New'
            task.save()
            return redirect('task_detail', id=task.id)
    else:
        form = TaskForm()
    
    context = {'form': form, 'user': user}
    return render(request, 'tasks/task_form.html', context)


# ==================== EDIT TASK (Manager only) ====================
@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def edit_task(request, id):
    task = get_object_or_404(Task, pk=id)
    user = request.user
    
    if user.role != 'Manager' or task.team != user.team:
        return redirect('task_list')
    
    # Only allow editing tasks with 'New' status
    if task.status != 'New':
        return redirect('task_detail', id=task.id)
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', id=task.id)
    else:
        form = TaskForm(instance=task)
    
    context = {'form': form, 'task': task}
    return render(request, 'tasks/task_form.html', context)


# ==================== UPDATE TASK STATUS ====================
@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def update_task_status(request, id):
    task = get_object_or_404(Task, pk=id)
    user = request.user
    
    if task.team != user.team:
        return redirect('task_list')
    
    # Employees can only update status of tasks assigned to them
    if user.role == 'Employee' and task.assigned_to != user:
        return redirect('task_detail', id=task.id)
    
    # Managers can only update status of tasks assigned to them
    if user.role == 'Manager' and task.assigned_to != user:
        return redirect('task_detail', id=task.id)
    
    if request.method == "POST":
        form = TaskStatusUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', id=task.id)
    else:
        form = TaskStatusUpdateForm(instance=task)
    
    context = {'form': form, 'task': task}
    return render(request, 'tasks/task_status_form.html', context)


# ==================== ASSOCIATE TASK (Assign to current user) ====================
@login_required(login_url='login')
def associate_task(request, id):
    """
    Associate Current User with an Unassigned Task
    - User can only associate themselves with unassigned tasks
    - Can only associate with tasks from their team
    - Redirects to task detail after association
    """
    task = get_object_or_404(Task, pk=id)
    user = request.user
    
    # Security: User can only associate with their team's tasks
    if task.team != user.team:
        return redirect('task_list')
    
    # Task must be unassigned
    if task.assigned_to is not None:
        return redirect('task_detail', id=task.id)
    
    # Assign task to current user
    task.assigned_to = user
    task.save()
    
    return redirect('task_detail', id=task.id)


# ==================== DELETE TASK (Manager only) ====================
@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def delete_task(request, id):
    task = get_object_or_404(Task, pk=id)
    user = request.user
    
    if user.role != 'Manager' or task.team != user.team:
        return redirect('task_list')
    
    if task.status != 'New':
        return redirect('task_detail', id=task.id)
    
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    
    context = {'task': task}
    return render(request, 'tasks/task_confirm_delete.html', context)

