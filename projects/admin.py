from django.contrib import admin
from .models import Project, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_date')
    search_fields = ('name', 'description')
    list_filter = ('created_date',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'priority', 'status', 'due_date')
    search_fields = ('title', 'description')
    list_filter = ('priority', 'status', 'due_date')
