from rest_framework import permissions

from apps.accounts.models import UserRole, AuthStatus


class IsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.user_role == UserRole.MANAGER and request.user.auth_status == AuthStatus.DONE


class IsEmployee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.user_role == UserRole.EMPLOYEE and request.user.auth_status == AuthStatus.DONE


class IsDelivery(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.user_role == UserRole.DELIVERY and request.user.auth_status == AuthStatus.DONE


class IsClient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.user_role == UserRole.CLIENT and request.user.auth_status == AuthStatus.DONE
