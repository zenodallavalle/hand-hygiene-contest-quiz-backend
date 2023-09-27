from contextlib import nullcontext
from rest_framework import serializers
from main.models import AnswerEvent, ResultEvent, StartEvent


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class AutoAddRemoteAddressAndUserAgentMixin:
    def create(self, validated_data):
        validated_data["ip"] = get_client_ip(self.context["request"])
        validated_data["user_agent"] = self.context["request"].META.get(
            "HTTP_USER_AGENT"
        )
        return super().create(validated_data)


class StartEventSerializer(
    AutoAddRemoteAddressAndUserAgentMixin, serializers.ModelSerializer
):
    class Meta:
        model = StartEvent
        fields = "__all__"

    datetime = serializers.DateTimeField(read_only=True)
    device_uid = serializers.CharField(max_length=100)
    device_type = serializers.IntegerField(min_value=1, max_value=4, required=False)
    ip = serializers.CharField(max_length=100, read_only=True)
    user_agent = serializers.CharField(max_length=1000, read_only=True)
    referrer = serializers.CharField(max_length=1000, required=False, allow_null=True)

    latitude = serializers.FloatField(read_only=True)
    longitude = serializers.FloatField(read_only=True)

    recaptcha_token = serializers.CharField(max_length=2000)
    recaptcha_score = serializers.FloatField(read_only=True)

    quiz_uid = serializers.CharField(max_length=100)

    nickname = serializers.CharField(max_length=100)
    job = serializers.IntegerField(min_value=1, max_value=7)


class AnswerEventSerializer(
    AutoAddRemoteAddressAndUserAgentMixin, serializers.ModelSerializer
):
    class Meta:
        model = AnswerEvent
        fields = "__all__"

    datetime = serializers.DateTimeField(read_only=True)
    device_uid = serializers.CharField(max_length=100)
    device_type = serializers.IntegerField(min_value=1, max_value=4, required=False)
    ip = serializers.CharField(max_length=100, read_only=True)
    user_agent = serializers.CharField(max_length=1000, read_only=True)

    latitude = serializers.FloatField(read_only=True)
    longitude = serializers.FloatField(read_only=True)

    recaptcha_token = serializers.CharField(max_length=2000)
    recaptcha_score = serializers.FloatField(read_only=True)

    nickname = serializers.CharField(max_length=100)
    job = serializers.IntegerField(min_value=1, max_value=7)

    quiz_uid = serializers.CharField(max_length=100)

    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()
    question_text = serializers.CharField()
    answer_text = serializers.CharField()


class ResultEventSerializer(
    AutoAddRemoteAddressAndUserAgentMixin, serializers.ModelSerializer
):
    class Meta:
        model = ResultEvent
        fields = "__all__"

    datetime = serializers.DateTimeField(read_only=True)
    device_uid = serializers.CharField(max_length=100)
    device_type = serializers.IntegerField(min_value=1, max_value=4, required=False)
    ip = serializers.CharField(max_length=100, read_only=True)
    user_agent = serializers.CharField(max_length=1000, read_only=True)

    latitude = serializers.FloatField(read_only=True)
    longitude = serializers.FloatField(read_only=True)

    recaptcha_token = serializers.CharField(max_length=2000)
    recaptcha_score = serializers.FloatField(read_only=True)

    nickname = serializers.CharField(max_length=100)
    job = serializers.IntegerField(min_value=1, max_value=7)
    quiz_uid = serializers.CharField(max_length=100)

    marks = serializers.IntegerField()
