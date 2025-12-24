from rest_framework import serializers

class SearchResultSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    type = serializers.CharField()
    title = serializers.CharField()
    snippet = serializers.CharField()
