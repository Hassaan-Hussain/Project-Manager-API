from django.db import models
from django.conf import settings
from django.db import models
from django.db.models import Q


class TeamMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        ADMIN = "ADMIN", "Admin"
        MEMBER = "MEMBER", "Member"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships"
    )
    team = models.ForeignKey(
        'Team', on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.MEMBER
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'team'),
                name='unique_user_team_membership',
            ),
            models.UniqueConstraint(
                fields=('team',),
                condition=Q(role='ADMIN'),
                name='unique_admin_per_team',
            )
        ]

    def __str__(self):
        return self.user.username


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_teams"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    
class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=255, blank=True)
    created_by = models.ForeignKey(
        'Team', on_delete=models.CASCADE, related_name='projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Task(models.Model):       
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=255, blank=True)
    status = models.CharField(choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ],
    default='pending'
    )
    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, related_name='tasks'
    )
    due_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'title'],
                name='unique_task_constraint',
            ),
        ]

    def __str__(self):
        return f"{self.project.title}'s task: {self.title}"


class TaskAssignment(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="assignments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="task_assignments"
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_assignments",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("task", "user")