from rest_framework.permissions import BasePermission


class OrderPermission(BasePermission):
    def has_permission(self, request, view):
        if (
            request.method == "GET"
            and request.user.is_authenticated
            and request.user.is_staff
        ):
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ["UPDATE"] and (
            request.user == obj.customer or request.user.is_staff
        ):
            return True

        if request.method == "GET" and (
            request.user == obj.customer
            or request.user.is_staff
            or request.user.is_master
        ):
            return True

        return False
