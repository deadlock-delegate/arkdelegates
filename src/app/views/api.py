from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator
from app.models import Delegate, History
from app.sql import sql_delegates
from app.serializers import DelegateSerializer


class Delegates(View):
    def get(self, request, *args, **kwargs):
        page = int(self.request.GET.get('page', 1))

        delegates = Delegate.objects.raw(sql_delegates)
        delegates_list = list(delegates)

        paginator = Paginator(list(delegates_list), 71)
        delegates_paginated = paginator.get_page(page)
        delegates_results = DelegateSerializer(delegates_paginated, many=True).data
        return JsonResponse({
            'all_results': len(delegates_list),
            'total_pages': paginator.num_pages,
            'current_page': page,
            'delegates': delegates_results,
        }, safe=False)
