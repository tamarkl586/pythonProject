from django.contrib import admin

from App1.models import Task, Team, CustomUser

# Register your models here.
admin.site.register(Task)
admin.site.register(Team)
admin.site.register(CustomUser)