from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
 

 
router=DefaultRouter()
router.register(r'SuperAdmin',SuperAdminViewSet,basename='SuperAdmin')
router.register(r'RefreshTokenView',RefreshTokenView,basename='RefreshTokenView')

 
urlpatterns = [
   
    path('',include(router.urls)),
   
     
   
 
]