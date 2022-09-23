from rest_framework import serializers
from .models import Box

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ["id", "length", "width", "height", "created_on", "updated_on", "created_by", "updated_by"]