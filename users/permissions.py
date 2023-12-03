from rest_framework.permissions import BasePermission


class IsOwnerOrIsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        if (
            request.method == "GET"
            and request.user.is_authenticated
            and request.user.is_staff
        ):
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "UPDATE"] and (
            request.user.is_staff or obj.username == request.user.username
        ):
            return True

        return False
