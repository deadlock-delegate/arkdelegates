from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django.views import View

from app.models import Delegate
from app.serializers import DelegateSerializer
from app.sql import sql_delegates, sql_select_all_info_for_delegate


class Delegates(View):
    def get(self, request, delegate_slug=None, **kwargs):

        if delegate_slug:
            data = self._get_delegate(delegate_slug)
        else:
            data = self._get_delegates()

        return JsonResponse(data, safe=False)

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
        delegate_query = Delegate.objects.raw(sql_select_all_info_for_delegate, [delegate_slug])

        try:
            delegate = delegate_query[0]
        except IndexError:
            raise Http404('Delegate %s does not exist', delegate_slug)

        delegate_result = DelegateSerializer(delegate).data

        return {
            'delegate': delegate_result,
        }

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
