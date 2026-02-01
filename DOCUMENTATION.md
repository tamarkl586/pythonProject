# Task Management System - Complete Documentation

## Overview
A Django-based task management system with user authentication, team management, and role-based task operations.

---

## 1. VIEWS.PY - Function-Based Views

### Authentication Views

#### **register(request)**
```python
def register(request):
```
- **Purpose**: Allows new users to create an account
- **Methods**: GET (show form), POST (create account)
- **Flow**: 
  1. User fills out SignUpForm with username, email, password
  2. Account is created
  3. User is automatically logged in
  4. Redirected to `profile_setup` page
- **Template**: `registration/signup.html`

#### **user_login(request)**
```python
def user_login(request):
```
- **Purpose**: Authenticates existing users
- **Methods**: GET (show form), POST (authenticate)
- **Logic**:
  - If user has no team → redirect to `profile_setup`
  - If user has team → redirect to `task_list`
- **Template**: `registration/login.html`

#### **user_logout(request)**
```python
def user_logout(request):
```
- **Purpose**: Logs out the current user
- **Decorator**: `@login_required`
- **Result**: Redirects to home page

### Profile Views

#### **profile_setup(request)**
```python
def profile_setup(request):
```
- **Purpose**: First-time profile setup after registration
- **Methods**: GET (show form), POST (save profile)
- **Fields**:
  - Team (required)
  - Role (required): Manager or Employee
- **Decorator**: `@login_required`
- **Redirect**: After completion → `task_list`
- **Template**: `registration/profile_setup.html`

#### **edit_profile(request)**
```python
def edit_profile(request):
```
- **Purpose**: Update user's team and role
- **Methods**: GET (show form), POST (save changes)
- **Decorator**: `@login_required`
- **Redirect**: After saving → `profile_detail`
- **Template**: `profile/edit_profile.html`

#### **profile_detail(request)**
```python
def profile_detail(request):
```
- **Purpose**: Display user's profile information
- **Decorator**: `@login_required`
- **Shows**: Username, email, team, role
- **Template**: `profile/profile_detail.html`

### General Views

#### **home(request)**
```python
def home(request):
```
- **Purpose**: Landing page for all users
- **Logic**:
  - If logged in → show dashboard with task statistics
  - If not logged in → show welcome page with login/register links
- **Displays**: Task stats, recent tasks, assigned tasks
- **Template**: `home.html`
- **No login required** - publicly accessible

---

## 2. TASK MANAGEMENT VIEWS

### Reading Tasks

#### **task_list(request)**
```python
def task_list(request):
```
- **Purpose**: Display all tasks for user's team
- **Methods**: GET
- **Decorators**: `@login_required`
- **Features**:
  - Tasks ordered by due_date (soonest first)
  - Filter by status using query parameter: `?status=New`
  - Shows task statistics (total, new, in progress, completed)
- **Shows per task**: Title, description, due_date, status, assigned_to
- **Template**: `tasks/task_list.html`

#### **task_detail(request, id)**
```python
def task_detail(request, id):
```
- **Purpose**: Display single task details
- **Methods**: GET
- **Decorators**: `@login_required`
- **Security**: User can only view tasks from their team
- **Shows**:
  - Full title
  - Complete description
  - Due date
  - Status
  - Assigned person
  - Links to edit/delete (manager only)
  - Link to update status (if assigned)
- **Template**: `tasks/task_detail.html`

### Creating Tasks (Manager Only)

#### **create_task(request)**
```python
def create_task(request):
```
- **Purpose**: Create new task (managers only)
- **Methods**: GET (show form), POST (create)
- **Decorators**: `@login_required`
- **Access Control**: Only managers can create tasks
- **Fields**: Title, description, due_date
- **Auto-set**: 
  - `team` = user's team
  - `status` = 'New'
- **Redirect**: After creation → `task_detail`
- **Template**: `tasks/task_form.html`

### Editing Tasks (Manager Only)

#### **edit_task(request, id)**
```python
def edit_task(request, id):
```
- **Purpose**: Edit task details (managers only)
- **Methods**: GET (show form), POST (save)
- **Decorators**: `@login_required`
- **Access Control**: 
  - Only managers can edit
  - Can only edit tasks from their team
- **Fields**: Title, description, due_date
- **Cannot edit**: Status (use `update_task_status` instead)
- **Redirect**: After save → `task_detail`
- **Template**: `tasks/task_form.html`

#### **update_task_status(request, id)**
```python
def update_task_status(request, id):
```
- **Purpose**: Update task status
- **Methods**: GET (show form), POST (save)
- **Decorators**: `@login_required`
- **Access Rules**:
  - Employees: Can only update their assigned tasks
  - Managers: Can update any task in their team
- **Status Options**: New → In Progress → Completed
- **Template**: `tasks/task_status_form.html`

#### **delete_task(request, id)**
```python
def delete_task(request, id):
```
- **Purpose**: Delete task (managers only)
- **Methods**: GET (confirmation), POST (delete)
- **Decorators**: `@login_required`
- **Access Control**:
  - Only managers can delete
  - Can only delete tasks with status='New'
  - Cannot delete tasks in progress or completed
- **Redirect**: After deletion → `task_list`
- **Template**: `tasks/task_confirm_delete.html`

---

## 3. URLS.PY - URL ROUTING

```python
# Authentication
path('register/', views.register, name='register')
path('login/', views.user_login, name='login')
path('logout/', views.user_logout, name='logout')

# Profile
path('profile/setup/', views.profile_setup, name='profile_setup')
path('profile/edit/', views.edit_profile, name='edit_profile')
path('profile/', views.profile_detail, name='profile_detail')

# Home
path('', views.home, name='home')

# Tasks
path('tasks/', views.task_list, name='task_list')
path('tasks/create/', views.create_task, name='create_task')
path('tasks/<int:id>/', views.task_detail, name='task_detail')
path('tasks/<int:id>/edit/', views.edit_task, name='edit_task')
path('tasks/<int:id>/status/', views.update_task_status, name='update_task_status')
path('tasks/<int:id>/delete/', views.delete_task, name='delete_task')
```

---

## 4. TEMPLATES - HTML FILES

### Base Template: `base.html`
- Navigation bar with authentication status
- User dropdown menu
- Main content block
- Footer
- Bootstrap 5 styling
- Responsive design

### Registration & Login

| File | Purpose |
|------|---------|
| `registration/signup.html` | User registration form |
| `registration/login.html` | User login form |
| `registration/profile_setup.html` | First-time profile setup (team & role selection) |

### Profile Templates

| File | Purpose |
|------|---------|
| `profile/profile_detail.html` | View user profile information |
| `profile/edit_profile.html` | Edit user profile (team & role) |

### Task Templates

| File | Purpose |
|------|---------|
| `tasks/task_list.html` | Display all tasks with filtering by status |
| `tasks/task_detail.html` | View full task details |
| `tasks/task_form.html` | Create or edit task (title, description, due_date) |
| `tasks/task_status_form.html` | Update task status |
| `tasks/task_confirm_delete.html` | Confirm task deletion |

### Home Template
| File | Purpose |
|------|---------|
| `home.html` | Dashboard for logged-in users / Welcome page for guests |

---

## 5. USER WORKFLOWS

### New User Registration Flow
```
1. User visits /register/
2. Fill SignUpForm (username, email, password)
3. Account created, user logged in
4. Redirect to /profile/setup/
5. Select team and role
6. Redirect to /tasks/
7. View team's tasks
```

### Existing User Login Flow
```
1. User visits /login/
2. Enter credentials
3. If no team → Redirect to /profile/setup/
4. If has team → Redirect to /tasks/
```

### Manager Creates Task
```
1. Manager visits /tasks/create/
2. Fill TaskForm (title, description, due_date)
3. Task saved with status='New' and team=manager's_team
4. Redirect to task detail page
```

### Manager Edits Task
```
1. Manager visits /tasks/<id>/edit/
2. Edit TaskForm (title, description, due_date)
3. Save changes
4. Redirect to task detail page
```

### Employee Updates Task Status
```
1. Employee views task they're assigned to
2. Click "Change Status"
3. Select new status from dropdown
4. Save
5. Redirect to task detail
```

---

## 6. SECURITY FEATURES

### Authentication
- `@login_required` decorator on all protected views
- Automatic logout on logout page
- Session management

### Authorization
- Employees can only:
  - View tasks from their team
  - Update status of tasks assigned to them
  
- Managers can:
  - Create new tasks
  - Edit any task details
  - Update any task status
  - Delete new tasks (status='New')

- Team isolation:
  - Users can only see/modify tasks from their team

### Data Protection
- `get_object_or_404()` prevents unauthorized access to non-existent resources
- Team ownership verified before allowing operations
- Role verification before allowing manager-only actions

---

## 7. KEY FEATURES

✅ **User Registration & Login**
✅ **Team-based task organization**
✅ **Role-based access control** (Manager/Employee)
✅ **Task lifecycle** (New → In Progress → Completed)
✅ **Task filtering by status**
✅ **Task sorting by due date**
✅ **Profile management**
✅ **Dashboard with task statistics**
✅ **Responsive Bootstrap UI**

---

## 8. DATABASE MODELS REFERENCE

### CustomUser
- username
- email
- password
- team (ForeignKey to Team)
- role (Manager or Employee)

### Team
- name (unique)
- members (reverse relation)
- tasks (reverse relation)

### Task
- title
- description
- due_date
- status (New, In Progress, Completed)
- team (ForeignKey)
- assigned_to (ForeignKey to CustomUser, nullable)

---

## 9. QUICK REFERENCE

### View Access by Role

| View | Public | Employee | Manager |
|------|--------|----------|---------|
| home | ✅ | ✅ | ✅ |
| register | ✅ | ✅ | ✅ |
| login | ✅ | ✅ | ✅ |
| logout | ❌ | ✅ | ✅ |
| profile_setup | ❌ | ✅ | ✅ |
| edit_profile | ❌ | ✅ | ✅ |
| profile_detail | ❌ | ✅ | ✅ |
| task_list | ❌ | ✅ | ✅ |
| task_detail | ❌ | ✅ | ✅ |
| create_task | ❌ | ❌ | ✅ |
| edit_task | ❌ | ❌ | ✅ |
| update_task_status | ❌ | ✅* | ✅ |
| delete_task | ❌ | ❌ | ✅** |

*Employee can only update their assigned tasks
**Manager can only delete tasks with status='New'

---

Generated: January 31, 2026
