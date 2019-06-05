from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import StatusUpdate
from app.permissions import IsOwnerOrReadOnly
from app.views.api.serializers import NewsModelSerializer


class News(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, delegate_slug=None, *args, **kwargs):
        page = int(self.request.GET.get("page", 1))
        limit = int(self.request.GET.get("limit", 10))
        delegate_slug = delegate_slug or self.request.GET.get("delegate_slug")
        if limit > 50:
            limit = 50

        filters = {}
        if delegate_slug:
            filters.update({"delegate__slug": delegate_slug})

        news_queryset = StatusUpdate.objects.filter(**filters).order_by("-created")
        paginator = Paginator(news_queryset, limit)
        news_paginated = paginator.get_page(page)

        news = []
        for item in news_paginated.object_list:
            news.append(
                {
                    "delegate_name": item.delegate.name,
                    "title": item.title,
                    "message": item.message,
                    "created": item.created,
                }
            )

        return Response(
            {
                "all_results": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": page,
                "data": news,
            }
        )

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data.update({"delegate": request.user.delegate.id})
        serializer = NewsModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.create(validated_data=serializer.validated_data)
        return Response(model_to_dict(instance), status=201)

    def put(self, request, news_id, *args, **kwargs):
        news = get_object_or_404(StatusUpdate, id=news_id)
        self.check_object_permissions(self.request, news)
        serializer = NewsModelSerializer(news, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, news_id, *args, **kwargs):
        news = get_object_or_404(StatusUpdate, id=news_id)
        self.check_object_permissions(self.request, news)
        news.delete()
        return Response()
