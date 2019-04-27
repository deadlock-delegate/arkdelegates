from rest_framework.serializers import ModelSerializer

from app.models import Delegate


class DelegateModelSerializer(ModelSerializer):
    class Meta:
        model = Delegate
        exclude = ("id", "user")
        read_only_fields = ("user", "name", "slug", "address", "public_key", "created", "updated")
