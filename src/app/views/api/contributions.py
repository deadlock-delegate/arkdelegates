from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Contribution


class Contributions(APIView):
    def get(self, request, *args, **kwargs):
        page = int(self.request.GET.get("page", 1))
        limit = int(self.request.GET.get("limit", 10))
        delegate_slug = self.request.GET.get("delegate_slug")
        if limit > 50:
            limit = 50

        filters = {}
        if delegate_slug:
            filters.update({"delegate__slug": delegate_slug})

        contributions_queryset = Contribution.objects.filter(**filters).order_by("-created")
        paginator = Paginator(contributions_queryset, limit)
        contributions_paginated = paginator.get_page(page)

        contributions = []
        for contribution in contributions_paginated.object_list:
            contributions.append(
                {
                    "delegate_name": contribution.delegate.name,
                    "title": contribution.title,
                    "description": contribution.description,
                    "created": contribution.created,
                }
            )

        return Response(
            {
                "all_results": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": page,
                "data": contributions,
            }
        )
