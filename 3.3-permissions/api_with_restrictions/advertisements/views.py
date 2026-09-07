from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import (
    Advertisement, AdvertisementStatusChoices, Favorite
)
from advertisements.permissions import IsOwnerOrReadOnly, NotAuthorPermission
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    queryset = Advertisement.objects.none()

    def get_queryset(self):
        user = self.request.user

        is_favorite_param = self.request.query_params.get('is_favorite')

        if is_favorite_param == 'true':
            if not user.is_authenticated:
                return Advertisement.objects.none()

            favorite_ad_ids = (Favorite.objects.filter(user=user).
                               values_list('advertisement_id', flat=True))
            qs = Advertisement.objects.filter(id__in=favorite_ad_ids)
            return qs.order_by('-created_at')

        if not user.is_authenticated:
            return Advertisement.objects.filter(
                status__in=[
                    AdvertisementStatusChoices.OPEN,
                    AdvertisementStatusChoices.CLOSED
                ]
            )
        base_qs = Advertisement.objects.filter(
            Q(status__in=[
                AdvertisementStatusChoices.OPEN,
                AdvertisementStatusChoices.CLOSED
            ])
            | (Q(creator=user) & Q(status=AdvertisementStatusChoices.DRAFT)))
        return base_qs.order_by('-created_at')

    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[NotAuthorPermission]
    )
    def favorite(self, request, pk=None):
        """
        POST /api/advertisements/{id}/favorite/
        Добавить объявление в избранное.
        """

        advertisement = self.get_object()
        fav, created = Favorite.objects.get_or_create(
            user=request.user,
            advertisement=advertisement
        )
        if created:
            return Response(
                {'detail': 'Объявление добавлено в избранное'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'detail': 'Объявление уже было в избранном'},
            status=status.HTTP_200_OK
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        """
        DELETE /api/advertisements/{id}/favorite/
        Удалить объявление из избранного.
        """

        advertisement = self.get_object()
        deleted_count, _ = Favorite.objects.filter(
            user=request.user,
            advertisement=advertisement
        ).delete()

        if deleted_count > 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'detail': 'Объявление не найдено в избранном'},
            status=status.HTTP_404_NOT_FOUND
        )

    def get_permissions(self):
        """Получение прав для действий."""

        request = self.request

        if request.user and (
                request.user.is_staff or request.user.is_superuser
        ):
            if self.action in ['favorite', 'delete_favorite']:
                return [NotAuthorPermission()]
            return [IsAuthenticated()]
        if self.action == "create":
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrReadOnly()]
        if self.action in ['favorite', 'delete_favorite']:
            return [NotAuthorPermission()]
        return [IsOwnerOrReadOnly()]
