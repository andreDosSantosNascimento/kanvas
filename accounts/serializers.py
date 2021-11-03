from rest_framework import serializers


class UserSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    is_superuser = serializers.BooleanField()
    is_staff = serializers.BooleanField()
