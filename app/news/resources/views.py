from rest_framework import viewsets

from app.news.models import News
from app.news.resources.serializers import NewsSerializer
from app.news.service import NewsService
from core.utils.permissions import IsAdminOrReadOnly


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    service = NewsService()
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        data = serializer.validated_data
        self.service.create_news(**data)

    def perform_update(self, serializer):
        data = serializer.validate_data
        news = self.get_object()
        self.service.update_news(news=news, **data)

    def perform_destroy(self, instance):
        self.service.delete_news(instance)
