from django.conf import settings
from rest_framework import serializers
from core.models import Machine, Line, Data


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['line', 'value']


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = ['id', 'machine', 'name']


class MachineSerializer(serializers.ModelSerializer):
    lines = LineSerializer(many=True, read_only=True)

    class Meta:
        model = Machine
        fields = ['id', 'ip', 'lines']
