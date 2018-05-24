import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from app.forms import ContributionForm, NodeForm, ProposalForm, StatusUpdateForm
from app.models import Contribution, Node, StatusUpdate
from app.serializers import ContributionSerializer, NodeSerializer, StatusUpdateSerializer


class EditProposalView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        self.delegate = self.request.user.delegate
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return JsonResponse({
            'proposal': self.delegate.proposal
        })

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        form = ProposalForm(data)
        data = {}
        if form.is_valid():
            self.delegate.proposal = form.cleaned_data['proposal']
            self.delegate.save()
            data.update({'updated': True})
        else:
            data.update({
                'updated': False,
                'errors': form.errors
            })
        return JsonResponse(data)


class EditContributionView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        self.delegate = self.request.user.delegate
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        contribution = get_object_or_404(
            Contribution, id=request.GET.get('id'), delegate_id=self.delegate.id
        )
        data = ContributionSerializer(contribution).data
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        form = ContributionForm(data)
        data = {}
        if form.is_valid():
            Contribution.objects.create(
                delegate=self.delegate,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description']
            )
            data.update({'created': True})
        else:
            data.update({
                'created': False,
                'errors': form.errors
            })
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        contribution = get_object_or_404(
            Contribution, id=request.GET.get('id'), delegate_id=self.delegate.id
        )
        data = json.loads(request.body)
        form = ContributionForm(data)
        data = {}
        if form.is_valid():
            contribution.title = form.cleaned_data['title']
            contribution.description = form.cleaned_data['description']
            contribution.save()
            data.update({'updated': True})
        else:
            data.update({
                'updated': False,
                'errors': form.errors
            })
        return JsonResponse(data)

    def delete(self, request, *args, **kwargs):
        contribution = get_object_or_404(
            Contribution, id=request.GET.get('id'), delegate_id=self.delegate.id
        )
        contribution.delete()
        return JsonResponse({'deleted': True})


class EditNodeView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        self.delegate = self.request.user.delegate
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        node = get_object_or_404(
            Node, id=request.GET.get('id'), delegate_id=self.delegate.id
        )
        data = NodeSerializer(node).data
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        form = NodeForm(data)
        data = {}
        if form.is_valid():
            Node.objects.create(
                delegate=self.delegate,
                network=form.cleaned_data['network'],
                cpu=form.cleaned_data['cpu'],
                memory=form.cleaned_data['memory'],
                is_dedicated=form.cleaned_data['is_dedicated'],
                is_backup=form.cleaned_data['is_backup'],
            )
            data.update({'created': True})
        else:
            data.update({
                'created': False,
                'errors': form.errors
            })
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        node = get_object_or_404(
            Node, id=request.GET.get('id'), delegate_id=self.delegate.id
        )
        data = json.loads(request.body)
        form = NodeForm(data)
        data = {}
        if form.is_valid():
            node.network = form.cleaned_data['network']
            node.cpu = form.cleaned_data['cpu']
            node.memory = form.cleaned_data['memory']
            node.is_dedicated = form.cleaned_data['is_dedicated']
            node.is_backup = form.cleaned_data['is_backup']
            node.save()
            data.update({'updated': True})
        else:
            data.update({
                'updated': False,
                'errors': form.errors
            })
        return JsonResponse(data)

    def delete(self, request, *args, **kwargs):
        node = get_object_or_404(
            Node, id=request.GET.get('id'), delegate_id=self.delegate.id
        )
        node.delete()
        return JsonResponse({'deleted': True})


class StatusUpdateView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        self.delegate = self.request.user.delegate
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        status = get_object_or_404(
            StatusUpdate, id=request.GET.get('id'), delegate_id=self.delegate.id
        )
        data = StatusUpdateSerializer(status).data
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        form = StatusUpdateForm(data)
        data = {}
        if form.is_valid():
            StatusUpdate.objects.create(
                delegate=self.delegate,
                message=form.cleaned_data['message'],
            )
            data.update({'created': True})
        else:
            data.update({
                'created': False,
                'errors': form.errors
            })
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        update = get_object_or_404(
            StatusUpdate, id=request.GET.get('id'), delegate_id=self.delegate.id
        )
        data = json.loads(request.body)
        form = StatusUpdateForm(data)
        data = {}
        if form.is_valid():
            update.message = form.cleaned_data['message']
            update.save()
            data.update({'updated': True})
        else:
            data.update({
                'updated': False,
                'errors': form.errors
            })
        return JsonResponse(data)

    def delete(self, request, *args, **kwargs):
        update = get_object_or_404(
            StatusUpdate, id=request.GET.get('id'), delegate_id=self.delegate.id
        )
        update.delete()
        return JsonResponse({'deleted': True})
