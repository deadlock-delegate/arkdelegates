from datetime import datetime

import serpy

from django.core.exceptions import ValidationError


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
    uptime = FloatField()
    approval = FloatField()
    rank = IntegerField()
    forged = IntegerField()
    missed = IntegerField()
    voters = IntegerField()
    total_nodes_count = IntegerField()
    backup_nodes_count = IntegerField()
    contributions_count = IntegerField()
    voting_power = StringField()
    voters_zero_balance = IntegerField()
    voters_not_zero_balance = IntegerField()
    is_private = serpy.BoolField()


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
