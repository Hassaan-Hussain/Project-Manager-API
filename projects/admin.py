from django.contrib import admin

from .models import Project, Task, Team

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [TaskInline]



admin.site.register(Team)
admin.site.register(Task)
