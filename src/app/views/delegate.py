from django.http import Http404
from django.views.generic.base import TemplateView

from app.models import Delegate
from app.utils import is_staff
from app.sql import sql_delegate_all_info_via_slug
from app.forms import ContributionForm, NodeForm, ProposalForm, StatusUpdateForm


class DelegateView(TemplateView):
    template_name = 'delegate.html'

    def get_context_data(self, delegate_slug, **kwargs):
        context = super().get_context_data(**kwargs)

        delegate_query = Delegate.objects.raw(
            sql_delegate_all_info_via_slug, [delegate_slug, delegate_slug, delegate_slug]
        )
        try:
            delegate = delegate_query[0]
        except IndexError:
            raise Http404('Delegate %s does not exist', delegate_slug)

        delegate_qs = Delegate.objects.get(slug=delegate_slug)
        nodes = delegate_qs.nodes.filter(is_active=True)
        contributions = delegate_qs.contributions.all()
        updates = delegate_qs.status_updates.order_by('-created')

        if self.request.user.is_authenticated and hasattr(self.request.user, 'delegate'):
            logged_in_delegate = Delegate.objects.get(user_id=self.request.user.id)
            can_edit_delegate = Delegate.objects.filter(
                user_id=self.request.user.id,
                slug=delegate_slug
            ).exists()
        else:
            logged_in_delegate = None
            can_edit_delegate = None

        if can_edit_delegate:
            context.update({
                'contributionForm': ContributionForm(),
                'nodeForm': NodeForm(),
                'proposalForm': ProposalForm(),
                'updateForm': StatusUpdateForm(),
            })

        context.update({
            'seo': {
                'title': '{} @ ARKdelegates.io'.format(delegate.name),
                'description': (
                    "Check what {} delegate has done for the ark community, how many nodes it runs "
                    "and what's the proposal.".format(delegate.name)
                )
            },
            'delegate': delegate,
            'nodes': nodes,
            'contributions': contributions,
            'updates': updates,
            'is_staff': is_staff(self.request.user),
            'can_edit_delegate': can_edit_delegate,
            'logged_in_delegate': logged_in_delegate
        })

        return context
