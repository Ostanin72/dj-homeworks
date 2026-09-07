from rest_framework.permissions import (
    BasePermission, SAFE_METHODS, IsAuthenticated
)

from advertisements.models import AdvertisementStatusChoices


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Админы имеют полный доступ всегда
        if request.user.is_staff:
            return True
        if request.method in SAFE_METHODS:
            if obj.status == AdvertisementStatusChoices.DRAFT:
                return obj.creator == request.user
            return True
        return obj.creator == request.user


class NotAuthorPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return not obj.creator == request.user
