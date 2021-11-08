from rest_framework import serializers


class UsersInCoursesSeriealizers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()


class CourseSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    users = UsersInCoursesSeriealizers(many=True)
