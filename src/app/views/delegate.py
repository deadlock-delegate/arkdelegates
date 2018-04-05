from django.http import Http404
from django.views.generic.base import TemplateView
from app.models import Delegate
from app.utils import has_edit_permissions
from app.sql import sql_delegate_all_info


class DelegateView(TemplateView):
    template_name = "delegate.html"

    def get_context_data(self, delegate_slug, **kwargs):
        context = super().get_context_data(**kwargs)

        delegate_query =  Delegate.objects.raw(sql_delegate_all_info, [delegate_slug])
        try:
            delegate = delegate_query[0]
        except IndexError:
            raise Http404('Delegate %s does not exist', delegate_slug)

        nodes = Delegate.objects.get(slug=delegate_slug).nodes.filter(is_active=True)
        contributions = Delegate.objects.get(slug=delegate_slug).contributions.all()

        context.update({
            'seo': {
                'title': 'ARK Delegates - Find and follow ARK delegates',
                'description': (
                    'Find ARK delegates that you want to support and follow their progress.'
                )
            },
            'delegate': delegate,
            'nodes': nodes,
            'contributions': contributions,
            'can_edit': has_edit_permissions(self.request.user)
        })

        return context
