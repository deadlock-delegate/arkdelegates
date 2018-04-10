from django.http import Http404
from django.views.generic.base import TemplateView
from app.models import Delegate
from app.utils import has_edit_permissions
from app.sql import sql_delegate_all_info


class DelegateView(TemplateView):
    template_name = "delegate.html"

    def get_context_data(self, delegate_slug, **kwargs):
        context = super().get_context_data(**kwargs)

        delegate_query = Delegate.objects.raw(sql_delegate_all_info, [delegate_slug])
        try:
            delegate = delegate_query[0]
        except IndexError:
            raise Http404('Delegate %s does not exist', delegate_slug)

        delegate_qs = Delegate.objects.get(slug=delegate_slug)
        nodes = delegate_qs.nodes.filter(is_active=True)
        contributions = delegate_qs.contributions.all()

        if self.request.user.is_authenticated:
            logged_in_delegate = Delegate.objects.get(user_id=self.request.user.id)
            can_edit_delegate = Delegate.objects.filter(
                user_id=self.request.user.id,
                slug=delegate_slug
            ).exists()
        else:
            logged_in_delegate = None
            can_edit_delegate = None

        context.update({
            'seo': {
                'title': '{} @ ARKdelegates.io'.format(delegate.name),
                'description': (
                    'Check what {} delegate has done for the ark community, how many nodes it runs '
                    'and what proposal have they written.'.format(delegate.name)
                )
            },
            'delegate': delegate,
            'nodes': nodes,
            'contributions': contributions,
            'can_edit': has_edit_permissions(self.request.user),
            'can_edit_delegate': can_edit_delegate,
            'logged_in_delegate': logged_in_delegate
        })

        return context
