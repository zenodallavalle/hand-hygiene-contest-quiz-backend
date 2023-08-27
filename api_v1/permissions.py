from django.conf import settings
from rest_framework import permissions


class AuthKeyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "GET":
            return (
                hasattr(settings, "AUTH_KEY")
                and request.headers.get("authorization", None) == settings.AUTH_KEY
            )
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method != "GET":
            return (
                hasattr(settings, "AUTH_KEY")
                and request.headers.get("authorization", None) == settings.AUTH_KEY
            )
        return request.user.is_authenticated
