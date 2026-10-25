from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated

# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import TeamFilter

from .models import Project, Task, TaskAssignment, Team, TeamMembership
from .serializers import (
    ProjectSerializer,
    TaskAssignmentSerializer,
    TaskSerializer,
    TeamMembershipSerializer,
    TeamSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)
    


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_fields = ['name']
    ordering_fields = ['name']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_permissions(self):
            self.permission_classes = [AllowAny]
            if self.request.method == 'POST':
                self.permission_classes = [IsAuthenticated]
            return super().get_permissions()
    

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_permissions(self):
            self.permission_classes = [AllowAny]
            if self.request.method == 'POST':
                self.permission_classes = [IsAuthenticated]
            return super().get_permissions()
    

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # this is main branch edit
    # this is main branch edit2    # comment for new commit in feature branch

class TeamMembershipViewSet(viewsets.ModelViewSet):
    queryset = TeamMembership.objects.all()
    serializer_class = TeamMembershipSerializer


class TaskAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAssignment.objects.all()
    serializer_class = TaskAssignmentSerializer

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)
  

