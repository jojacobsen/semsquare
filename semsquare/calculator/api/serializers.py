from rest_framework import serializers

class LatentVariableSerializer(serializers.Serializer):
    name = serializers.CharField()
    mode = serializers.CharField()


class PlspmSerializer(serializers.Serializer):
    """Serializer for plspm"""
    data = serializers.DictField()
    #latentVariable = LatentVariableSerializer(many=True)

