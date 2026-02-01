"""
Script to create test data for the task management system
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskManagement.settings')
django.setup()

from App1.models import Team, CustomUser, Task

print("Creating test data...")

# Create teams
teams = []
team_names = ['Development', 'Design', 'QA']
for name in team_names:
    team, created = Team.objects.get_or_create(name=name)
    teams.append(team)

# Create a manager user for testing
manager_user, created = CustomUser.objects.get_or_create(
    username='testmanager',
    defaults={
        'email': 'manager@example.com',
        'team': teams[0],
        'role': 'Manager',
    }
)
if created:
    manager_user.set_password('password123')
    manager_user.save()

# Create an employee user for testing
employee_user, created = CustomUser.objects.get_or_create(
    username='testemployee',
    defaults={
        'email': 'employee@example.com',
        'team': teams[0],
        'role': 'Employee',
    }
)
if created:
    employee_user.set_password('password123')
    employee_user.save()

# Create sample tasks
task_data = [
    ('Fix login bug', 'Fix the authentication issue', 3),
    ('Design dashboard', 'Create a new dashboard design', 5),
    ('Update API', 'Add new API endpoints', 7),
    ('Test features', 'QA testing for new release', None),
    ('Write docs', 'Update documentation', 2),
]

team = teams[0]
for idx, (title, desc, days) in enumerate(task_data):
    due_date = datetime.now().date() + timedelta(days=days) if days else datetime.now().date() + timedelta(days=10)
    task, created = Task.objects.get_or_create(
        title=title,
        team=team,
        defaults={
            'description': desc,
            'due_date': due_date,
            'status': ['New', 'In Progress', 'Completed'][idx % 3],
            'assigned_to': employee_user if idx % 2 == 0 else None,
        }
    )

print("✅ Test data created!")
print(f"Teams: {', '.join([t.name for t in teams])}")
print(f"Users: testmanager (Manager), testemployee (Employee)")
print(f"Tasks: {Task.objects.count()} tasks created")

