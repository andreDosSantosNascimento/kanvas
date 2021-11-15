from rest_framework import serializers


class SubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    grade = serializers.IntegerField()
    repo = serializers.CharField()
    user_id = serializers.IntegerField()
    activity_id = serializers.IntegerField()


class ActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    points = serializers.IntegerField()
    submissions = SubmissionSerializer(many=True)
