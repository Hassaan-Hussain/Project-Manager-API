from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Team, Project, Task, TeamMembership, TaskAssignment

# Create your tests here.

class UserAPITest(APITestCase):
    def setUp(self):
        self.hassaan = User.objects.create_user(username='Hassaan', password='H@has321')
        self.bilal = User.objects.create_user(username='Bilal', password='H@has321')
        self.awais = User.objects.create_user(username='Awais', password='H@has321')

    def test_user_list_required_authentication(self):
        response = self.client.get('http://localhost:8000/api/v1/user/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication_user_only_sees_their_own_user(self):
        token = RefreshToken.for_user(self.hassaan).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('http://localhost:8000/api/v1/user/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.hassaan.id)

    def test_authenticated_use_cannot_retrieve_another_user(self):
        token = RefreshToken.for_user(self.hassaan).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(f'http://localhost:8000/api/v1/user/{self.bilal.id}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TeamAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Hassaan",
            password="test-password",
        )
        self.team = Team.objects.create(
            name="Cogent",
            created_by=self.user,
        )

    def test_any_user_can_retrieve_all_teams(self):
        response = self.client.get("http://127.0.0.1:8000/api/v1/team/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_authenticated_user_can_create_team(self):
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post(
            '/api/v1/team/',
            {
                "name": "CodeWingz",
                "created_by_user": self.user.id
            },
            format="json",
        )   

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
