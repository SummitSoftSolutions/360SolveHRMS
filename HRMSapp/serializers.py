from rest_framework import serializers
from .models import *

class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        models=SuperAdmin
        fields='__all__'