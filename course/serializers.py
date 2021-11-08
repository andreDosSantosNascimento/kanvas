from rest_framework import serializers
from accounts.serializers import UserSerializers


class CourseSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    users = UserSerializers(many=True)
