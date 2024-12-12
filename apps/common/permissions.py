from rest_framework import permissions

from apps.accounts.models import UserRole


class IsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.user_role == UserRole.MANAGER


class IsEmployee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.user_role == UserRole.EMPLOYEE


class IsDelivery(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.user_role == UserRole.DELIVERY


class IsClient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.user_role == UserRole.CLIENT
