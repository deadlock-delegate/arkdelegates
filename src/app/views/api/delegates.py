from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.permissions import IsOwnerOrReadOnly
from app.models import Delegate
from app.serializers import DelegateSerializer
from app.sql import sql_delegates, sql_select_all_info_for_delegate
from app.views.api.serializers import DelegateModelSerializer


class Delegates(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, delegate_slug=None, *args, **kwargs):
        if delegate_slug:
            data = self._get_delegate(delegate_slug)
        else:
            data = self._get_delegates()
        return Response(data)

    def put(self, request, delegate_slug=None, **kwargs):
        delegate = get_object_or_404(Delegate, slug=delegate_slug)

        # Check permissions, if user has permissions to change data for a delegate
        self.check_object_permissions(self.request, delegate)

        serializer = DelegateModelSerializer(delegate, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=204)

    def _get_delegate(self, delegate_slug):
        """
        Gets data for a specific delegate

        Args:
            delegate_slug (string): delegate slug

        Returns:
            json: JSON object containing all delegate information

        Raises:
            Http404: if delegate with given delegate slug does not exist
        """
        delegates_list = cache.get('app.sql.get_delegate.{}'.format(delegate_slug))
        if not delegates_list:
            delegates = Delegate.objects.raw(sql_select_all_info_for_delegate, [delegate_slug])
            delegates_list = list(delegates)
            cache.set('app.sql.get_delegate.{}'.format(delegate_slug), delegates_list, 5 * 60)

        try:
            delegate = delegates_list[0]
        except IndexError:
            raise Http404('Delegate %s does not exist', delegate_slug)

        delegate_result = DelegateSerializer(delegate).data

        return delegate_result

    def _get_delegates(self):
        """
        Gets all delegates. It shows up to 60 delegates per page.

        Returns:
            json: JSON object containing all delegates
        """
        page = int(self.request.GET.get('page', 1))

        delegates_list = cache.get('app.sql.get_delegates')
        if not delegates_list:
            delegates = Delegate.objects.raw(sql_delegates)  # todo: optimize this raw sql yo
            delegates_list = list(delegates)
            cache.set('app.sql.get_delegates', delegates_list, 5 * 60)  # expire cache in 5min

        paginator = Paginator(delegates_list, 60)
        delegates_paginated = paginator.get_page(page)
        delegates_results = DelegateSerializer(delegates_paginated, many=True).data

        return {
            'all_results': len(delegates_list),
            'total_pages': paginator.num_pages,
            'current_page': page,
            'delegates': delegates_results,
        }
