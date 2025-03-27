from rest_framework import serializers
from .models import *

class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        models=SuperAdmin
        fields='__all__'
        

class ModuleSerializer(serializers.Serializer):
    class Meta:
        models=MasterModule
        fields='__all__'