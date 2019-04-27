from datetime import datetime

from django.core.exceptions import ValidationError
from django.db.models import Count, Q

import serpy

from app.models import Delegate


class DateTimeField(serpy.Field):
    def to_value(self, value):
        if not value:
            return
        elif not isinstance(value, datetime):
            raise ValidationError('Value must be of type datetime')
        return value.isoformat()


class StringField(serpy.Field):
    def to_value(self, value):
        if not value:
            return
        elif not isinstance(value, str):
            raise ValidationError('Value must be of type string')
        return value


class IntegerField(serpy.Field):
    def to_value(self, value):
        if not value:
            return
        return value


class FloatField(serpy.Field):
    def to_value(self, value):
        if not value:
            return
        return value


class DelegateSerializer(serpy.Serializer):
    id = IntegerField()
    name = StringField()
    address = StringField()
    created = DateTimeField()
    updated = DateTimeField()
    proposal = StringField()
    website = StringField()
    approval = FloatField()
    rank = IntegerField()
    rank_changed = IntegerField()
    forged = IntegerField()
    voters = IntegerField()
    total_nodes_count = IntegerField()
    backup_nodes_count = IntegerField()
    contributions_count = IntegerField()
    voting_power = StringField()
    voters_zero_balance = IntegerField()
    voters_not_zero_balance = IntegerField()
    is_private = serpy.BoolField()

    payout_covering_fee = serpy.BoolField()
    payout_percent = FloatField()
    payout_interval = IntegerField()
    payout_minimum = StringField()
    payout_maximum = StringField()
    payout_minimum_vote_amount = StringField()
    payout_maximum_vote_amount = StringField()


class ContributionSerializer(serpy.Serializer):
    title = StringField()
    description = StringField()


class NodeSerializer(serpy.Serializer):
    network = StringField()
    cpu = StringField()
    memory = StringField()
    is_dedicated = serpy.BoolField()
    is_backup = serpy.BoolField()


class StatusUpdateSerializer(serpy.Serializer):
    message = StringField()


class DelegateInfo(serpy.DictSerializer):

    id = IntegerField()
    name = StringField()
    slug = StringField()
    address = StringField()
    public_key = StringField()
    created = DateTimeField()
    updated = DateTimeField()
    website = StringField()
    proposal = StringField()
    is_private = serpy.BoolField()
    payout_covering_fee = serpy.BoolField()
    payout_percent = FloatField()
    payout_interval = IntegerField()
    payout_minimum = StringField()
    payout_maximum = StringField()
    payout_minimum_vote_amount = StringField()
    payout_maximum_vote_amount = StringField()
    user_id = IntegerField()

    approval = FloatField()
    rank = IntegerField()
    rank_changed = IntegerField()
    forged = IntegerField()
    voters = IntegerField()
    voting_power = StringField()

    total_nodes_count = IntegerField()
    backup_nodes_count = IntegerField()
    contributions_count = IntegerField()
    voters_zero_balance = IntegerField()
    voters_not_zero_balance = IntegerField()

    @classmethod
    def from_slug(cls, slug, *args, **kwargs):
        total_node_count_query = Count('nodes', filter=Q(nodes__is_active=True), distinct=True)
        backup_node_count_query = Count(
            'nodes', filter=Q(nodes__is_active=True, nodes__is_backup=True), distinct=True
        )
        contributions_count_query = Count('contributions', distinct=True)
        delegate = (
            Delegate.objects
            .annotate(total_nodes_count=total_node_count_query)
            .annotate(backup_nodes_count=backup_node_count_query)
            .annotate(contributions_count=contributions_count_query)
            .get(slug=slug)
        )

        data = {
            'id': delegate.id,
            'name': delegate.name,
            'slug': delegate.slug,
            'address': delegate.address,
            'public_key': delegate.public_key,
            'created': delegate.created,
            'updated': delegate.updated,
            'website': delegate.website,
            'proposal': delegate.proposal,
            'is_private': delegate.is_private,
            'payout_covering_fee': delegate.payout_covering_fee,
            'payout_percent': delegate.payout_percent,
            'payout_interval': delegate.payout_interval,
            'payout_minimum': delegate.payout_minimum,
            'payout_maximum': delegate.payout_maximum,
            'payout_minimum_vote_amount': delegate.payout_minimum_vote_amount,
            'payout_maximum_vote_amount': delegate.payout_maximum_vote_amount,
            'user_id': delegate.user_id,

            'total_nodes_count': delegate.total_nodes_count,
            'backup_nodes_count': delegate.backup_nodes_count,
            'contributions_count': delegate.contributions_count,

            'approval': None,
            'rank': None,
            'rank_changed': None,
            'forged': None,
            'voters': None,
            'voting_power': None,
            'voters_zero_balance': None,
            'voters_not_zero_balance': None,
        }

        history = delegate.histories.order_by('-created').first()
        if history:
            data['approval'] = history.approval
            data['rank'] = history.rank
            data['rank_changed'] = history.rank_changed
            data['forged'] = history.forged
            data['voters'] = history.voters
            data['voting_power'] = history.voting_power
            data['voters_zero_balance'] = history.payload.get('voters_zero_balance')
            data['voters_not_zero_balance'] = history.payload.get('voters_not_zero_balance')

        return DelegateInfo(data)
