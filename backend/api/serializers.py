from rest_framework import serializers
from .models import Ciclovia

class CicloviaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciclovia
        fields = '__all__'
