from rest_framework.serializers import ModelSerializer

from app.models import Contribution, Delegate, StatusUpdate


class DelegateModelSerializer(ModelSerializer):
    class Meta:
        model = Delegate
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "name",
            "slug",
            "address",
            "public_key",
            "created",
            "updated",
        )


class NewsModelSerializer(ModelSerializer):
    class Meta:
        model = StatusUpdate
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")


class ContributionModelSerializer(ModelSerializer):
    class Meta:
        model = Contribution
        fields = "__all__"
        read_only_fields = ("id", "created")


class DelegatePayoutModelSerializer(ModelSerializer):
    class Meta:
        model = Delegate
        fields = [
            "payout_covering_fee",
            "payout_percent",
            "payout_interval",
            "payout_minimum",
            "payout_maximum",
            "payout_minimum_vote_amount",
            "payout_maximum_vote_amount",
        ]
