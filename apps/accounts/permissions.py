from rest_framework import permissions, status
from rest_framework.response import Response

from apps.accounts.models import UserRole, AuthStatus


class IsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not (request.user.user_role == UserRole.MANAGER and request.user.auth_status == AuthStatus.DONE):
            return Response(
                data={
                    'success': False,
                    'message': "You do not have permission to perform this action, restaurant MANAGER only"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return request.user


class IsEmployee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.user_role != UserRole.EMPLOYEE and request.user.auth_status != AuthStatus.DONE:
            return Response(
                data={
                    'success': False,
                    'message': "You do not have permission to perform this action, branch EMPLOYEE only"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return request.user


class IsDelivery(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not (request.user.user_role == UserRole.DELIVERY and request.user.auth_status == AuthStatus.DONE):
            return Response(
                data={
                    'success': False,
                    'message': "You do not have permission to perform this action, DELIVERY only"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return request.user


class IsClient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not (request.user.user_role == UserRole.CLIENT and request.user.auth_status == AuthStatus.DONE):
            return Response(
                data={
                    'success': False,
                    'message': "You do not have permission to perform this action, CLIENT only"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return request.user
