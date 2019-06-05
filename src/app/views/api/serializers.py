from rest_framework.serializers import ModelSerializer

from app.models import Contribution, Delegate, StatusUpdate


class DelegateModelSerializer(ModelSerializer):
    class Meta:
        model = Delegate
        exclude = ("id", "user")
        read_only_fields = ("user", "name", "slug", "address", "public_key", "created", "updated")


class NewsModelSerializer(ModelSerializer):
    class Meta:
        model = StatusUpdate
        exclude = ("id",)
        read_only_fields = ("created", "updated")


class ContributionModelSerializer(ModelSerializer):
    class Meta:
        model = Contribution
        exclude = ("id",)
        read_only_fields = ("created",)
