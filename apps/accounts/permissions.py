from rest_framework import permissions

from apps.accounts.models import UserRole, AuthStatus


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                request.user.user_role == UserRole.OWNER and
                request.user.auth_status == AuthStatus.DONE
        )



class IsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                request.user.user_role != UserRole.MANAGER and
                request.user.auth_status != AuthStatus.DONE
        )


class IsCourier(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                request.user.user_role == UserRole.COURIER and
                request.user.auth_status == AuthStatus.DONE
        )



class IsClient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                    request.user.user_role == UserRole.CLIENT and
                    request.user.auth_status == AuthStatus.DONE
        )

