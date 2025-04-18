from django.urls import path,include,re_path
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

schema_view = get_schema_view(
    openapi.Info(
        title='HRMS API',
        default_version='v1',
        description="HR Management System API Documentation",
    ),
    public=True,
    permission_classes=(AllowAny,)
)


 
router=DefaultRouter()
router.register(r'SuperAdmin',SuperAdminViewSet,basename='SuperAdmin'),
router.register(r'RefreshTokenView',RefreshTokenView,basename='RefreshTokenView'),
router.register(r'ModuleViewSet',ModuleViewSet,basename='ModuleViewSet'),
router.register(r'CreatSubmodule',CreatSubmodule,basename='CreatSubmodule'),
router.register(r'SubmoduleLimitCreation',SubmoduleLimitCreation,basename='SubmoduleLimitCreation'),
router.register(r'VoucherCreation',VoucherCreation,basename='VoucherCreation'),
router.register(r'GroupAdmincreation',GroupAdmincreation,basename='GroupAdmincreation'),
router.register(r'SubmoduleList',SubmoduleList,basename='SubmoduleList')
router.register(r'TaxTypeViewSet',TaxTypeViewSet,basename='TaxTypeViewSet')
router.register(r"TaxCategory",TaxCategory,basename='TaxCategory')


 
urlpatterns = [
   
    path('',include(router.urls)),
    # path('ModuleViewSet/<int:pk>/partial_update/', ModuleViewSet.as_view({'patch': 'partial_update'}), name='module-partial-update'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
      
    

]
