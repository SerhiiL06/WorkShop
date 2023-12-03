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
        if request.method == "PUT":
            return True

        if request.method == "GET" and (
            request.user == obj.customer
            or request.user.is_staff
            or request.user.is_master
        ):
            return True

        return False


class IsMasterOrIsStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if (
            request.method == "GET"
            and (request.user.is_master and request.user == obj.master)
            or request.user.is_staff
        ):
            return True

        return False
