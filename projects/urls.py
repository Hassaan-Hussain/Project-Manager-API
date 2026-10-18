from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


router = DefaultRouter()

router.register('user', views.UserViewSet, basename='user')
router.register('team', views.TeamViewSet, basename='team')
router.register('project', views.ProjectViewSet, basename='project')
router.register('task', views.TaskViewSet, basename='task')
router.register('team-membership', views.TeamMembershipViewSet, basename='team-membership')
router.register('task-assignment', views.TaskAssignmentViewSet, basename='task-assignment')

urlpatterns = router.urls

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]