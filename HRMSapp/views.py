from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets,status
from .serializers import *
from  rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

# Generating user token




# Create your views here.
class SuperAdminViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def create(self, request):
        print("Received OTP verification request!")  
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = SuperAdmin.objects.get(email=email,Password=password)
            print(f"User found: {user.email}")  

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
 
            print(f"Tokens generated: access={access_token}, refresh={refresh_token}")  
 
            return Response({
                "status": "success",
                "message": "OTP verified successfully!",
                "access_token": access_token,
                "refresh_token": refresh_token
            }, status=status.HTTP_200_OK)
 
        except SuperAdmin.DoesNotExist:
            print("User not found!")  
            return Response({"status": "error", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


