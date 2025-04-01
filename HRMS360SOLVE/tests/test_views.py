import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from HRMSapp.models import SuperAdmin

User = get_user_model()

@pytest.fixture
def api_client():
    """Fixture for API client"""
    return APIClient()

@pytest.fixture
def create_super_admin(db):
    """Fixture to create a test SuperAdmin user"""
    user = SuperAdmin.objects.create(email="admin@example.com", Password="testpassword")
    return user

@pytest.fixture
def generate_tokens(create_super_admin):
    """Fixture to generate JWT tokens for a test user"""
    refresh = RefreshToken.for_user(create_super_admin)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}

@pytest.mark.django_db
def test_superadmin_login_success(api_client, create_super_admin):
    """Test successful login for SuperAdmin"""
    response = api_client.post("/SuperAdmin/", {"email": "admin@example.com", "password": "testpassword"})
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.data

@pytest.mark.django_db
def test_superadmin_login_failure(api_client):
    """Test failed login due to incorrect credentials"""
    response = api_client.post("/SuperAdmin/", {"email": "wrong@example.com", "password": "wrongpass"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["message"] == "User not found"

@pytest.mark.django_db
def test_refresh_token_success(api_client, generate_tokens):
    """Test refreshing the access token with a valid refresh token"""
    api_client.cookies["refresh_token"] = generate_tokens["refresh"]
    response = api_client.post("/RefreshTokenView/")
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.data

@pytest.mark.django_db
def test_refresh_token_invalid(api_client):
    """Test refresh token failure with an invalid token"""
    api_client.cookies["refresh_token"] = "invalid_token"
    response = api_client.post("/RefreshTokenView/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["message"] == "Invalid refresh token"
