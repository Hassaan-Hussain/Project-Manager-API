from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as validate_django_password
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers

from .models import Project, Task, TaskAssignment, Team, TeamMembership

User = get_user_model()



class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(
        source='created_by.name',
        read_only=True, 
    )
    created_by_team = serializers.PrimaryKeyRelatedField(
        source='created_by', 
        queryset=Team.objects.all(), 
        write_only=True
    )
    
    class Meta: 
        model = Project
        fields = ['title', 'description', 'created_by', 'created_by_team', 'created_at']
        read_only_fields = ['created_at']


class TeamSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(
        source = 'created_by.username',
        read_only=True,
    )
    created_by_user = serializers.PrimaryKeyRelatedField(
        source='created_by',
        queryset=User.objects.all(),
        write_only=True,
    )
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_by', 'created_by_user', 'created_at']
        read_only_fields = ['created_by', 'created_at']


class TeamMembershipSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        source = 'user.username',
    )
    team = serializers.CharField(
        source = 'team.name',
    )
    
    class Meta:
        model = TeamMembership
        fields = ['pk', 'user', 'team', 'role', 'joined_at']
        read_only_fields = ['joined_at']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'last_login',
            'date_joined',
        ]
        read_only_fields = ['id', 'last_login', 'date_joined']

    def validate_password(self, value):
        try:
            validate_django_password(value, user=self.instance)
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.messages)
        return value

    def validate(self, attrs):
        if self.instance is None and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'This field is required when creating a user.'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        groups = validated_data.pop('groups', [])
        user_permissions = validated_data.pop('user_permissions', [])
        user = User.objects.create_user(password=password, **validated_data)
        user.groups.set(groups)
        user.user_permissions.set(user_permissions)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        write_only = True,
    )
    project_title = serializers.CharField(
        source = 'project.title',
        read_only = True,
    )
    class Meta:
        model = Task
        fields = [
            'pk',
            'title',
            'description',
            'status',
            'project',
            'project_title',
            'due_date',
        ]


class TaskAssignmentSerializer(serializers.ModelSerializer):
    task = serializers.CharField(
        source='task.title',
        read_only=True
    )
    task_id = serializers.PrimaryKeyRelatedField(
        source='task',
        queryset=Task.objects.all(),
        write_only=True,
    )
    project = serializers.CharField(
        source='task.project.title',
        read_only=True,
    )
    user = serializers.CharField(
        source='user.username',
        read_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.all(),
        write_only=True,
    )
    assigned_by = serializers.CharField(
        source='assigned_by.username',
        read_only=True,
    )

    class Meta:
        model = TaskAssignment
        fields = [
            'id',
            'project',
            'task',
            'task_id',
            'user',
            'user_id',
            'assigned_by',
            'assigned_at',
        ]
        read_only_fields = ['id', 'assigned_at']
    