from django.views.generic.base import TemplateView
from app.models import Contribution


class Contributions(TemplateView):
    template_name = "contributions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        contributions = Contribution.objects.all().order_by('-created', '-id')

        context.update({
            'seo': {
                'title': 'Latests contributions to ARK from delegates @ ARKdelegates.io',
                'description': (
                    'List of all contributions done to ARK by ARK delegates'
                )
            },
            'contributions': contributions
        })

        return context
