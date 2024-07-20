from rest_framework import serializers
from . import models

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Documents
        fields = '__all__'

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Query
        fields = '__all__'