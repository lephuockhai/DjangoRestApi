from rest_framework import serializers
from .models import TokenInfomation

class TokenInfomationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenInfomation
        fields = '__all__'