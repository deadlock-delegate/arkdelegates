from django.http import HttpResponse
from django.views.generic.base import TemplateView

from app.delegate_utils import fetch_delegates
from app.utils import is_staff


def health(request):
    """Return a 200 status code when the service is healthy.
    This endpoint returning a 200 means the service is healthy, anything else
    means it is not. It is called frequently and should be fast.
    """
    return HttpResponse('')


class Homepage(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))
        search_query = self.request.GET.get('search', '')

        delegates, paginator = fetch_delegates(page, search_query=search_query)

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
            'delegates': delegates,
            'is_staff': is_staff(self.request.user),
            'paginator': paginator,
            'logged_in_delegate': logged_in_delegate,
            'search': search_query,
        })

        return context
