from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_v1.views import StartEventViewSet, AnswerEventViewSet, ResultEventViewSet

router = DefaultRouter()
router.register(r"start_event", StartEventViewSet)
router.register(r"answer_event", AnswerEventViewSet)
router.register(r"result_event", ResultEventViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
