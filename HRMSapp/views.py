from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets,status
from .serializers import *
from  rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from  drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .kafka_producer import send_hrm_event
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser

User = get_user_model()
# Create your views here.
class SuperAdminViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, example="user@example.com"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, example="123456"),
            },
            required=['email', 'password']
        ),
        responses={
            200: openapi.Response("Success", openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, example="success"),
                'message': openapi.Schema(type=openapi.TYPE_STRING, example="Logged successfully!"),
                'access_token': openapi.Schema(type=openapi.TYPE_STRING, example="your_access_token"),
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, example="your_refresh_token"),
            })),
            400: "Invalid  data",
            404: "User not found"
        }
    )
    def create(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = SuperAdmin.objects.get(email=email,password=password)
 
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
 
            print(f"Tokens generated: access={access_token}, refresh={refresh_token}")  
            response = Response({
                "status": "success",
                "message": "Logged in successfully!",
                "access_token": access_token,
            }, status=status.HTTP_200_OK)
            response.set_cookie(key="refresh_token",value=refresh_token,httponly=True,secure=True,samesite='Lax')
            return response
 
        except SuperAdmin.DoesNotExist:
            print("User not found!")  
            return Response({"status": "error", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class RefreshTokenView(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def create(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        print("cookies",refresh_token)
        if not refresh_token:
            return Response({'status':"error","message":"No refreshtoken provided"},status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh =RefreshToken(refresh_token)
            access_token =str(refresh.access_token)
            return Response({"acess":access_token},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':"error","message":"Invalid refresh token"},status=status.HTTP_401_UNAUTHORIZED)
        

class ModuleViewSet(viewsets.ViewSet):
    permission_classes=[AllowAny]
    parser_classes = [MultiPartParser, FormParser]  # Enable file upload parsing

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Name', openapi.IN_FORM, description="Module Name", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('Logo', openapi.IN_FORM, description="Upload Logo", type=openapi.TYPE_FILE, required=True),
            openapi.Parameter('IsDeleted', openapi.IN_FORM, description="Is Deleted (0 or 1)", type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('Status', openapi.IN_FORM, description="Status (0: Inactive, 1: Active, 2: Pending)", type=openapi.TYPE_INTEGER, required=False),
        ]
    )
    def create(self, request):
        name = request.data.get("Name")
        logo = request.FILES.get("Logo")  
        is_deleted = request.data.get("IsDeleted", 0)
        status_value = request.data.get("Status", 1)

        if not name or not logo:
            return Response({"error": "Name and Logo are required."}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "Name": name,
            "Logo": logo,
            "IsDeleted": is_deleted,
            "Status": status_value,
        }

        serializer = MasterModuleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def list(self,request):
        try:
            data = MasterModule.objects.all()
            
            if not data.exists():
                Response({"message":"No records found"},status=status.HTTP_404_NOT_FOUND)
                
            serializer = MasterModuleSerializer(data,many=True)
        except Exception as e:
            return Response(
                {"error":"Something went wrong","details":str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        
    
    
    


