from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Contribution
from app.permissions import IsOwnerOrReadOnly
from app.views.api.serializers import ContributionModelSerializer


class Contributions(APIView):
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

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data.update({"delegate": request.user.delegate.id})
        serializer = ContributionModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.create(validated_data=serializer.validated_data)
        return Response(data=model_to_dict(instance), status=201)

    def put(self, request, contribution_id, *args, **kwargs):
        contribution = get_object_or_404(Contribution, id=contribution_id)
        self.check_object_permissions(self.request, contribution)
        serializer = ContributionModelSerializer(contribution, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def delete(self, request, contribution_id, *args, **kwargs):
        contribution = get_object_or_404(Contribution, id=contribution_id)
        self.check_object_permissions(self.request, contribution)
        contribution.delete()
        return Response()
