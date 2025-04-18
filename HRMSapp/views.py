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
# from .kafka_producer import send_hrm_event
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

# Token Mixins

class TokenMixin:
    def extract_token(self, request):
        """Helper method to extract and decode the token."""
        header = request.headers.get('Authorization')
        if not header:
            return None  # Or raise an exception if token is missing
        token = header.split()[1]
        decoded_token = UntypedToken(token)  # Decodes the token and returns a dictionary-like object
        return decoded_token
        

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
            user = User.objects.get(email=email)
            if not check_password(password,user.password):
                return Response({"error":"Invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)
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
            response.set_cookie(key="refresh_token",value=refresh_token,httponly=True,secure=False,samesite='None')
            return response
 
        except User.DoesNotExist:
            return Response({"status": "error", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    


        
        
''' Submodules '''
class CreatSubmodule(viewsets.ViewSet,TokenMixin):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'Name': openapi.Schema(type=openapi.TYPE_STRING, example="Name"),
                'Module': openapi.Schema(type=openapi.TYPE_STRING, example="1"),
            },
            required=['Name', 'Module']
        ),
        responses={
            200: SubModuleSerializer(many=True),
            404: openapi.Response("No records found"),
            500: openapi.Response("Something went wrong"),
        }
    )
    def create(self,request):
        try:
            data ={
                "Name":request.data.get('Name'),
                # "limit":request.data.get('Limit'),
                "Module":request.data.get('Module')
            }
            module_data = SubModuleSerializer(data = data)
            if module_data.is_valid():
                module_data.save()
                return Response(module_data.data,status=status.HTTP_201_CREATED)
            else:
                return Response(module_data.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"{e}",status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'module_id',
            openapi.IN_QUERY,
            description="ID of the module",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response("Success", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, example="success"),
                'message': openapi.Schema(type=openapi.TYPE_STRING, example="Loaded successfully!"),
               
                
            }
        )),
        400: "Invalid data",
            404: "Data not found"
        }
    )
    def list(self,request):
        permission_classes = [AllowAny]
        token_data = self.extract_token(request)
        if not token_data:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        id_data = token_data.get('user_id')
        print("id_data", id_data)
        module_id = request.query_params.get('module_id')
        if module_id:
            sub_data = SubModule.objects.filter(Module=module_id)
        serializer  = SubModuleSerializer(sub_data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
            
    
    def retrieve(self,request,pk=None):
        item = SubModule.objects.get(id = pk)
        token_data = self.extract_token(request)
        user_id = token_data.get('id')
        print("user_id",user_id)
        serializer = SubModuleSerializer(item)
        return Response(serializer.data)
    
    def destroy(self,request,pk=None):
        item = get_object_or_404(SubModule,id=pk)
        item.IsDeleted = 1
        item.save()
        return Response({"message": "SubModule marked as deleted."}, status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self,request,pk=None):
        item = get_object_or_404(SubModule,id=pk)
        serializer = SubModuleSerializer(data=request.data,instance=item,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ModuleViewSet(viewsets.ViewSet):
    permission_classes=[AllowAny]
    parser_classes = [MultiPartParser, FormParser]  # Enable file upload parsing

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Name', openapi.IN_FORM, description="Module Name", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('Description', openapi.IN_FORM, description="Description", type=openapi.TYPE_STRING, required=True),
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
    
    @swagger_auto_schema(
        operation_description="Retrieve all master modules",
        responses={
            200: MasterModuleSerializer(many=True),
            404: openapi.Response("No records found"),
            500: openapi.Response("Something went wrong"),
        }
    )
    def list(self,request):
        permission_classes=[AllowAny]
        parser_classes=[MultiPartParser,FormParser]
        try:
            data = MasterModule.objects.filter(IsDeleted=0)
            print("data:---",data)
            
            if not data.exists():
                return Response({"message":"No records found"},status=status.HTTP_404_NOT_FOUND)
                
            serializer = MasterModuleSerializer(data,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"Something went wrong","details":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
            request_body=MasterModuleSerializer 
        )
    def partial_update(self, request, pk=None):
        authentication_classes = [JWTAuthentication] 
        permission_classes = [IsAuthenticated]
        try:
            update_data = MasterModule.objects.get(pk=pk)
        except MasterModule.DoesNotExist:
            return Response({"message": "No records found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MasterModuleSerializer(update_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Module Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            user = MasterModule.objects.get(id=pk,IsDeleted=0)
            serializer = MasterModuleSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"No recordss found"},status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self,request,pk=None):
        try:
            query_set = MasterModule.objects.get(id=pk,IsDeleted=0)
            print("module:",query_set)
            query_set.IsDeleted = 1
            query_set.save()
            return Response({'message':"module deleted sucessfully.."},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
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
    
    
    
        
        
class SubmoduleLimitCreation(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def create(self,request):
        try:
            submod = request.data.get('submod')
            limit_value = request.data.get('limit_value')
            print("limit_value",limit_value,submod)
            sub_id =  SubModule.objects.get(id  = submod)
            sub_id_data =  sub_id.id
            data = {
                "submod":sub_id_data,
                "limit_value":limit_value
            }
            sub_data  = SubModuleLimitSerializer(data=data)
            if sub_data.is_valid():
                sub_data.save()
                return Response({"status":"success"},status=status.HTTP_200_OK)
            else:
                return Response({"error":sub_data.errors},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error":"Data error"},status=status.HTTP_401_UNAUTHORIZED)
        
    
    def retrieve(self,request,pk=None):
        if pk is None:
            return Response({"error":"Id's not provided"})
        try:        
            sub_data = SubmoduleLimit.objects.get(submod=pk)
        except SubmoduleLimit.DoesNotExist :
            return Response({"status":"Data doesn't exist"})        
        sub_serializer = SubModuleLimitSerializer(sub_data)
        return Response(sub_serializer.data)
    
            
    def destroy(self,request,pk=None):
        if pk is None:
            return Response({"error":"Id's not provided"})
        try:        
            sub_data = SubmoduleLimit.objects.get(submod=pk)
        except SubmoduleLimit.DoesNotExist :
            return Response({"status":"Data doesn't exist"})        
        sub_data.isdeleted = 1
        sub_data.save()
        return Response({"status":"Successfully deleted"})
    
    
    
class TaxCategory(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=TaxCategorySerializer
    )
    def create(self,request):
        try:
            name= request.data.get("name")
            
            data= {
                "name":name,
            }
            serializer = TaxCategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"created sucessfully..."},status=status.HTTP_201_CREATED)
            return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        
        

class TaxTypeViewSet(viewsets.ViewSet):
    @ swagger_auto_schema(
        request_body=TaxTypeSerializer
    )
    def create(self,request):
        try:
            taxName = request.data.get('taxName')
            Category=request.data.get('Category')
            
            data = {
                "taxName":taxName,
                "Category":Category,
            }
            
            serializer = TaxTypeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"created sucessfully.."},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
                
        
            

# Voucher creation

class VoucherCreation(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def create(self,request):
        data = request.data
        voucher_data = VouchertypeSerializer(data = data)
        if voucher_data.is_valid():
            voucher_data.save()
            return Response({"status":"success"},status=status.HTTP_200_OK)
        else:
            return Response({"status":"error"},status=status.HTTP_400_BAD_REQUEST)
            

class GroupAdmincreation(viewsets.ViewSet):
    def create(self,request):
        data = request.data
        group_data = GroupadminSerializer(data=data)
        if group_data.is_valid():
            group_data.save()
            return Response({"status":"success"},status=status.HTTP_200_OK)
        else:
            return Response({"status":"error"},status=status.HTTP_400_BAD_REQUEST)
        
    

class SubmoduleList(viewsets.ViewSet,TokenMixin):
    permission_classes = [AllowAny]
    def list(self,request):
        token_data = self.extract_token(request)
        if not token_data:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        sub_data = SubModule.objects.all()
        serializer  = SubModuleSerializer(sub_data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)