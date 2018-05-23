from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from app.forms import StatusUpdateForm
from app.models import Delegate, StatusUpdate
from app.utils import is_staff


class UpdateView(TemplateView):
    template_name = "update.html"

    def get_context_data(self, delegate_slug, update_id, **kwargs):
        context = super().get_context_data(**kwargs)

        delegate = get_object_or_404(Delegate, slug=delegate_slug)
        update = get_object_or_404(StatusUpdate, id=update_id, delegate_id=delegate.id)

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
                'updateForm': StatusUpdateForm(),
            })

        context.update({
            'seo': {
                'title': 'Status update from {} @ ARKdelegates.io'.format(delegate.name),
                'description': update.message
            },
            'delegate': delegate,
            'update': update,
            'is_staff': is_staff(self.request.user),
            'can_edit_delegate': can_edit_delegate,
            'logged_in_delegate': logged_in_delegate
        })

        return context
