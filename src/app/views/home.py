from django.http import HttpResponse
from django.core.cache import cache
from django.views.generic.base import TemplateView
from app.models import Delegate
from app.utils import is_staff
from app.sql import sql_delegates
from django.core.paginator import Paginator


def health(request):
    """Return a 200 status code when the service is healthy.
    This endpoint returning a 200 means the service is healthy, anything else
    means it is not. It is called frequently and should be fast.
    """
    return HttpResponse('')


class Homepage(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        delegates_list = cache.get('app.sql.get_delegates')
        if not delegates_list:
            delegates = Delegate.objects.raw(sql_delegates)  # todo: optimize this raw sql yo
            delegates_list = list(delegates)
            cache.set('app.sql.get_delegates', delegates_list, 5 * 60)  # expire cache in 5min

        page = int(self.request.GET.get('page', 1))
        paginator = Paginator(delegates_list, 60)
        delegates_paginated = paginator.get_page(page)

        if self.request.user.is_authenticated and hasattr(self.request.user, 'delegate'):
            logged_in_delegate = self.request.user.delegate
        else:
            logged_in_delegate = None

        context.update({
            'seo': {
                'title': 'ARK delegates - Find and follow ARK delegates',
                'description': (
                    'Find ARK delegates you want to support. See what they are doing, what have '
                    'they done and follow their progress.'
                )
            },
            'delegates': delegates_paginated,
            'is_staff': is_staff(self.request.user),
            'paginator': delegates_paginated,
            'logged_in_delegate': logged_in_delegate
        })

        return context
