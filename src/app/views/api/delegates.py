from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from app.delegate_utils import fetch_delegates
from app.models import Delegate
from app.permissions import IsOwnerOrReadOnly
from app.serializers import DelegateInfo
from app.views.api.serializers import DelegateModelSerializer


class Delegates(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, delegate_slug=None, wallet_address=None, *args, **kwargs):
        if wallet_address:
            # todo: support fetching delegate via wallet address
            raise Http404()
        elif delegate_slug:
            data = self._get_delegate(delegate_slug)
        else:
            data = self._get_delegates()
        return Response(data)

    def put(self, request, delegate_slug=None, wallet_address=None, **kwargs):
        if wallet_address:
            delegate = get_object_or_404(Delegate, address=wallet_address)
        else:
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
        delegate_result = DelegateInfo.from_slug(delegate_slug).data
        return delegate_result

    def _get_delegates(self):
        """
        Gets all delegates. It shows up to 60 delegates per page.

        Returns:
            json: JSON object containing all delegates
        """
        page = int(self.request.GET.get('page', 1))

        delegates, paginator = fetch_delegates(page)
        return {
            'all_results': paginator.paginator.count,
            'total_pages': paginator.paginator.num_pages,
            'current_page': page,
            'delegates': delegates,
        }
