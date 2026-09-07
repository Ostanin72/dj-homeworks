from rest_framework.permissions import (
    BasePermission, SAFE_METHODS, IsAuthenticated
)

from advertisements.models import AdvertisementStatusChoices


class IsOwnerOrReadOnly(BasePermission):
    """ Основной прав доступа."""

    def has_object_permission(self, request, view, obj):
        # Админы имеют полный доступ всегда
        if request.user.is_staff:
            return True

        if request.method in SAFE_METHODS:
            # просматривать объявления со статусом DRAFT может только автор
            if obj.status == AdvertisementStatusChoices.DRAFT:
                return obj.creator == request.user
            # просматривать остальные объявления могут все
            return True
        # Создавать, изменять, удалять объявления может только автор
        return obj.creator == request.user


class NotAuthorPermission(IsAuthenticated):
    """ Права доступа у всех, кроме автора объявления"""

    def has_object_permission(self, request, view, obj):
        return not obj.creator == request.user
