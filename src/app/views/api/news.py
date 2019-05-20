from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import StatusUpdate


class News(APIView):
    def get(self, request, delegate_slug=None, *args, **kwargs):
        page = int(self.request.GET.get("page", 1))
        limit = int(self.request.GET.get("limit", 10))
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
