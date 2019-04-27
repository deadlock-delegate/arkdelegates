from datetime import timedelta

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils import timezone

from app.models import Delegate, History
from app.serializers import DelegateInfo


def fetch_delegates(page, search_query=None):
    total_node_count_query = Count(
        'delegate_fk__nodes', filter=Q(delegate_fk__nodes__is_active=True), distinct=True)
    backup_node_count_query = Count(
        'delegate_fk__nodes',
        filter=Q(delegate_fk__nodes__is_active=True, delegate_fk__nodes__is_backup=True),
        distinct=True
    )
    contributions_count_query = Count('delegate_fk__contributions', distinct=True)

    base_query = History.objects.filter(created__gt=timezone.now() - timedelta(days=3))
    if search_query:
        base_query = History.objects.filter(
            Q(delegate_fk__name__icontains=search_query) | Q(delegate_fk__address=search_query)
        )

    history_ids = (
        base_query
        .order_by('delegate_fk', '-created')
        .distinct('delegate_fk')
        .values_list('id', flat=True)
    )

    histories = (
        History.objects.all()
        .filter(id__in=history_ids)
        .annotate(total_nodes_count=total_node_count_query)
        .annotate(backup_nodes_count=backup_node_count_query)
        .annotate(contributions_count=contributions_count_query)
        .select_related('delegate_fk')
        .order_by('rank')
    )

    paginator = Paginator(histories, 60)
    histories_paginated = paginator.get_page(page)

    delegates = []
    for history in histories_paginated.object_list:
        data = {
            'id': history.delegate_fk.id,
            'name': history.delegate_fk.name,
            'slug': history.delegate_fk.slug,
            'address': history.delegate_fk.address,
            'public_key': history.delegate_fk.public_key,
            'created': history.delegate_fk.created,
            'updated': history.delegate_fk.updated,
            'website': history.delegate_fk.website,
            'proposal': history.delegate_fk.proposal,
            'is_private': history.delegate_fk.is_private,
            'payout_covering_fee': history.delegate_fk.payout_covering_fee,
            'payout_percent': history.delegate_fk.payout_percent,
            'payout_interval': history.delegate_fk.payout_interval,
            'payout_minimum': history.delegate_fk.payout_minimum,
            'payout_maximum': history.delegate_fk.payout_maximum,
            'payout_minimum_vote_amount': history.delegate_fk.payout_minimum_vote_amount,
            'payout_maximum_vote_amount': history.delegate_fk.payout_maximum_vote_amount,
            'user_id': history.delegate_fk.user_id,

            'total_nodes_count': history.total_nodes_count,
            'backup_nodes_count': history.backup_nodes_count,
            'contributions_count': history.contributions_count,

            'approval': history.approval,
            'rank': history.rank,
            'rank_changed': history.rank_changed,
            'forged': history.forged,
            'voters': history.voters,
            'voting_power': history.voting_power,
            'voters_zero_balance': history.payload.get('voters_zero_balance'),
            'voters_not_zero_balance': history.payload.get('voters_not_zero_balance'),
        }
        delegates.append(data)

    return DelegateInfo(instance=delegates, many=True).data, histories_paginated


def fetch_new_delegates():
    delegates = Delegate.objects.exclude(
        proposal=None
    ).exclude(
        user_id=None
    ).order_by('-created')[:6]
    base_query = History.objects.filter(
        created__gt=timezone.now() - timedelta(days=3),
        delegate_fk__in=delegates.values_list('id')
    )

    history_ids = (
        base_query
        .order_by('delegate_fk', '-created')
        .distinct('delegate_fk')
        .values_list('id', flat=True)
    )

    total_node_count_query = Count(
        'delegate_fk__nodes', filter=Q(delegate_fk__nodes__is_active=True), distinct=True)
    backup_node_count_query = Count(
        'delegate_fk__nodes',
        filter=Q(delegate_fk__nodes__is_active=True, delegate_fk__nodes__is_backup=True),
        distinct=True
    )
    contributions_count_query = Count('delegate_fk__contributions', distinct=True)

    histories = (
        History.objects.all()
        .filter(id__in=history_ids)
        .annotate(total_nodes_count=total_node_count_query)
        .annotate(backup_nodes_count=backup_node_count_query)
        .annotate(contributions_count=contributions_count_query)
        .select_related('delegate_fk')
        .order_by('-delegate_fk__created')
    )

    delegates_data = []
    for history in histories:
        data = {
            'id': history.delegate_fk.id,
            'name': history.delegate_fk.name,
            'slug': history.delegate_fk.slug,
            'address': history.delegate_fk.address,
            'public_key': history.delegate_fk.public_key,
            'created': history.delegate_fk.created,
            'updated': history.delegate_fk.updated,
            'website': history.delegate_fk.website,
            'proposal': history.delegate_fk.proposal,
            'is_private': history.delegate_fk.is_private,
            'payout_covering_fee': history.delegate_fk.payout_covering_fee,
            'payout_percent': history.delegate_fk.payout_percent,
            'payout_interval': history.delegate_fk.payout_interval,
            'payout_minimum': history.delegate_fk.payout_minimum,
            'payout_maximum': history.delegate_fk.payout_maximum,
            'payout_minimum_vote_amount': history.delegate_fk.payout_minimum_vote_amount,
            'payout_maximum_vote_amount': history.delegate_fk.payout_maximum_vote_amount,
            'user_id': history.delegate_fk.user_id,

            'total_nodes_count': history.total_nodes_count,
            'backup_nodes_count': history.backup_nodes_count,
            'contributions_count': history.contributions_count,

            'approval': history.approval,
            'rank': history.rank,
            'rank_changed': history.rank_changed,
            'forged': history.forged,
            'voters': history.voters,
            'voting_power': history.voting_power,
            'voters_zero_balance': history.payload.get('voters_zero_balance'),
            'voters_not_zero_balance': history.payload.get('voters_not_zero_balance'),
        }
        delegates_data.append(data)

    return DelegateInfo(instance=delegates_data, many=True).data
