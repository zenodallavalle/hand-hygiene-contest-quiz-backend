from rest_framework import viewsets
from rest_framework import permissions
from api_v1.permissions import AuthKeyPermission

from main.models import StartEvent, AnswerEvent, ResultEvent
from api_v1.serializer import (
    StartEventSerializer,
    AnswerEventSerializer,
    ResultEventSerializer,
)

ALLOWED_METHODS = [
    # "get",
    "post",
    # "put",
    # "patch",
    # "delete",
    # "head",
    # "options",
]


class StartEventViewSet(viewsets.ModelViewSet):
    queryset = StartEvent.objects.all()
    serializer_class = StartEventSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ALLOWED_METHODS
    permission_classes = [AuthKeyPermission]


class AnswerEventViewSet(viewsets.ModelViewSet):
    queryset = AnswerEvent.objects.all()
    serializer_class = AnswerEventSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ALLOWED_METHODS
    permission_classes = [AuthKeyPermission]


class ResultEventViewSet(viewsets.ModelViewSet):
    queryset = ResultEvent.objects.all()
    serializer_class = ResultEventSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ALLOWED_METHODS
    permission_classes = [AuthKeyPermission]
