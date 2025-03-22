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
        email = request.data.get("email")
        password = request.data.get("password")
        
        try:
            # Retrieve user
            user = SuperAdmin.objects.get(email=email, Password=password)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            
            # Creating response and setting the cookie
            response = Response({
                "status": "success",
                "message": "OTP verified successfully!",
                "access_token": access_token,
            }, status=status.HTTP_200_OK)

            # Setting the refresh token cookie
            response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=False, samesite='None')
            

            return response
        except SuperAdmin.DoesNotExist:
            return Response({"status": "error", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    

class RefreshTokenView(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def create(self, request):
        refresh_token = request.COOKIES.get('refresh_token')  # Get from cookie
        if not refresh_token:
            return Response({"status": "error", "message": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

        

