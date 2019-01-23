from rest_framework import serializers
from . import models




class BackendSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'description',
        )
        # model = models.Backend

