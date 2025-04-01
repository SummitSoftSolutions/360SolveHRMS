from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"
        

class MasterModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model=MasterModule
        fields='__all__'
        

class SubModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubModule
        fields='__all__'