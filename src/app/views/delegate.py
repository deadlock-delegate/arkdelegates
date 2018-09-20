from django.views.generic.base import TemplateView

from app.forms import ContributionForm, NodeForm, ProposalForm, StatusUpdateForm
from app.models import Contribution, Delegate, Node, StatusUpdate
from app.serializers import DelegateInfo
from app.utils import is_staff


class DelegateView(TemplateView):
    template_name = 'delegate.html'

    def get_context_data(self, delegate_slug, **kwargs):
        context = super().get_context_data(**kwargs)

        delegate_info = DelegateInfo.from_slug(delegate_slug).data

        nodes = Node.objects.filter(delegate_id=delegate_info['id'], is_active=True)
        contributions = Contribution.objects.filter(delegate_id=delegate_info['id'])
        updates = StatusUpdate.objects.filter(delegate_id=delegate_info['id']).order_by('-created')

        if self.request.user.is_authenticated and hasattr(self.request.user, 'delegate'):
            logged_in_delegate = Delegate.objects.get(user_id=self.request.user.id)
            can_edit_delegate = Delegate.objects.filter(
                user_id=self.request.user.id,
                slug=delegate_slug
            ).exists()
        else:
            logged_in_delegate = None
            can_edit_delegate = True

        if can_edit_delegate:
            context.update({
                'contributionForm': ContributionForm(),
                'nodeForm': NodeForm(),
                'proposalForm': ProposalForm(),
                'updateForm': StatusUpdateForm(),
            })

        context.update({
            'seo': {
                'title': '{} @ ARKdelegates.io'.format(delegate_info['name']),
                'description': (
                    'Check what {} delegate has done for the Ark community, how many nodes it runs '
                    "and what's the proposal.".format(delegate_info['name'])
                )
            },
            'delegate': delegate_info,
            'nodes': nodes,
            'contributions': contributions,
            'updates': updates,
            'is_staff': is_staff(self.request.user),
            'can_edit_delegate': can_edit_delegate,
            'logged_in_delegate': logged_in_delegate,
        })

        return context
