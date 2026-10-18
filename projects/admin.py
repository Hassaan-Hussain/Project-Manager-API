from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Project, Task, Team, TeamMembership, TaskAssignment

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0

admin.site.unregister(User)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'team_names'
    )
    @admin.display(description="Teams")
    def team_names(self, obj):
        return ", ".join(
            membership.team.name
            for membership in obj.memberships.select_related("team").all()
        )

    add_fieldsets = (
        (None, {
            'fields':(
                'first_name',
                'last_name',
                'username',
                'email', 
                'password1',
                'password2',
            )
        }),
    )
    

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [TaskInline]



@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'team', 'role']
    list_display_links = ['user']
    ordering = ['user__username']

class TeamAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'created_by']

admin.site.register(TaskAssignment)
admin.site.register(Team, TeamAdmin)
admin.site.register(Task)
