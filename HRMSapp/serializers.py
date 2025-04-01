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
        
class SubLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubModule
        fields= ['id','Name']
        

class SubModuleLimitSerializer(serializers.ModelSerializer):
    submod = SubLimitSerializer()
    class Meta:
        model = SubmoduleLimit
        fields = ['id', 'limit_value', 'isactive', 'isdeleted', 'submod']