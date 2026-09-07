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

    # заглушка для маршрутизатора Django REST Framework (DRF).
    queryset = Advertisement.objects.none()

    # метод динамически формирует выборку объявлений
    # в зависимости от прав пользователя и параметров запроса
    def get_queryset(self):
        # Определяет текущего пользователя из запроса
        user = self.request.user

        is_favorite_param = self.request.query_params.get('is_favorite')
        # Фильтрация по избранному
        if is_favorite_param == 'true':
            # анонимные пользователи не могут иметь список избранного
            if not user.is_authenticated:
                return Advertisement.objects.none()

            # авторизованных пользователей выполняется подзапрос к модели Favorite
            favorite_ad_ids = (Favorite.objects.filter(user=user).
                               values_list('advertisement_id', flat=True))
            qs = Advertisement.objects.filter(id__in=favorite_ad_ids)
            return qs.order_by('-created_at')

        # Анонимные пользователи видят только объявления
        # со статусом OPEN или CLOSED
        if not user.is_authenticated:
            return Advertisement.objects.filter(
                status__in=[
                    AdvertisementStatusChoices.OPEN,
                    AdvertisementStatusChoices.CLOSED
                ]
            )
        # Авторизованные пользователи видят только объявления
        # со статусом OPEN или CLOSED
        # авторы видят еще и свои объявления со статусом DRAFT
        base_qs = Advertisement.objects.filter(
            Q(status__in=[
                AdvertisementStatusChoices.OPEN,
                AdvertisementStatusChoices.CLOSED
            ])
            | (Q(creator=user) & Q(status=AdvertisementStatusChoices.DRAFT)))
        return base_qs.order_by('-created_at')

    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    # сохранения объекта перед его записью в базу данных
    # только от имени текущего пользователя
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    #
    @action(
        detail=True,
        methods=['post'],
        # Автор не может добавить свое собственное объявление в избранное
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
