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
    Module = MasterModuleSerializer()
    class Meta:
        model=SubModule
        fields= ['id','Name','IsDeleted','Module']
        
class SubLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubModule
        fields= ['id','Name']
        

class SubModuleLimitSerializer(serializers.ModelSerializer):
    submod = SubLimitSerializer()
    class Meta:
        model = SubmoduleLimit
        fields = ['id', 'limit_value', 'isactive', 'isdeleted', 'submod']
        
        

class VouchertypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=VoucherTypeTbl
        fields= "__all__"
        
        
class GroupadminSerializer(serializers.ModelSerializer):
    class Meta:
        model=Groupadmin
        fields= "__all__"
    
class TaxTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxType
        fields = "__all__"
    
class TaxCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxCategory
        fields="__all__"
