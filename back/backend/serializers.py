# Rupika Dikkala
# January 23, 2019
# File contains serializers needed
# to set up API end points

from rest_framework import serializers
from . import models

# serializer for reports
class ReportSerializer(serializers.ModelSerializer):
    # user id is foreign key...? fix this
    user_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        fields = list()
        model = models.Report

        if model.submitted:
            fields = (
                'user_id',
                'title',
                'date_created',
                'data_submitted',
                'submitted',
            )
        else:
            fields = (
                'user_id',
                'title',
                'date_created',
                'submitted',
            )


# section serializer
class SectionSerializer(serializers.ModelSerializer):
    # report id foriegn key
    report_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


    class Meta:
        fields = (
            'report_id',
            'completed',
            'title',
            'html_description',
            'number',
        )
        model = models.Section


class FieldSerializer(serializers.ModelSerializer):
    # section_id is foriegn key
    section_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        fields = (
            'section_id',
            'label',
            'number',
            'type',
            'completed',
        )
        model = models.Field


class DataSerializer(serializers.ModelSerializer):
    field_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)








