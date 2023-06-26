from django.conf import settings
from rest_framework import permissions


class AuthKeyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.headers.get("authorization", None) == settings.AUTH_KEY
        except Exception:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            return request.headers.get("authorization", None) == settings.AUTH_KEY
        except Exception:
            return False
