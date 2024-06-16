import pytest
import pytest_django
from rest_framework.test import APIClient
from users.models import User
from knox.models import AuthToken


class TestUser:

    def setup(self):
        self.client = APIClient()

    @pytest.mark.django_db()
    @pytest.mark.parametrize('username,password,email,status', [
        ['test1', 'testingthepassword', 'test5@test.com', 200],
        ['test6', 'testingthepassword24', 'test5@test.com', 200],
        ['test7', 'Testing,thepassword.', 'test7@test.com', 200],
    ])
    def test_register_user(self, username, password, email, status):
        request = self.client.post('/users/register/', {'username': username, 'password': password, 'email': email})
        assert request.status_code == status
        assert request.data['token'] is not None

    # Test re-registering a user
    @pytest.mark.django_db()
    @pytest.mark.parametrize('username,password,email,status', [
        ['test1', 'testingthepassword', 'test5@test.com', 400],
        ['test6', 'testingthepassword23', 'test6@test.com', 400],
        ['test7', 'Testing,thepassword', 'test7@test.com', 400],
    ])
    def test_already_registered(self, username, password, email, status):
        self.client.post('/users/register/', {'username': username, 'password': password, 'email': email})
        request = self.client.post('/users/register/', {'username': username, 'password': password, 'email': email})
        assert request.status_code == status

    # Testing login
    @pytest.mark.django_db()
    @pytest.mark.parametrize('username,password,email,status', [
        ['test', 'testing', 'test5@test.com', 200],
        ['test6', 'testingthepassword23', 'test6@test.com', 200],
    ])
    def test_login(self, username, password, email, status):
        User.objects.create_user(username=username,password=password,email=email)
        request = self.client.post('/users/login/', {'username': username, 'password': password})
        assert request.status_code == status
        assert request.data['username'] == username