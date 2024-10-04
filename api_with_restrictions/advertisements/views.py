from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from rest_framework.response import Response
from .filters import AdvertisementFilter
from .models import Advertisement
from .permissions import OwnerOrRead
from .serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    pagination_class = [OwnerOrRead]
    filter_backends = [filters.DjangoFilterBackend]
    filter_fields = ['created_at', 'creator', 'status']
    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [OwnerOrRead()]
        return []


    def list(self, request, **kwargs):
        queryset = Advertisement.objects.all()
        queryset = AdvertisementFilter(data=request.GET, queryset=queryset, request=request).qs
        serializer = AdvertisementSerializer(queryset, many=True)
        return Response(serializer.data)