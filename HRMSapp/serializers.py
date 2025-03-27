from rest_framework import serializers
from .models import *

class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model=SuperAdmin
        fields='__all__'
        

class MasterModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model=MasterModule
        fields='__all__'