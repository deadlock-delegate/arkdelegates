from django.contrib.auth import get_user_model
import factory

from app import models


class UserFactory(factory.django.DjangoModelFactory):
    # Having random stuff in factories usually causes issues.Let's try it, but
    # if it'll cause problems, we should get rid of randomness in factories.
    username = factory.Faker("slug")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")

    class Meta:
        model = get_user_model()


class DelegateFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Faker("word")
    address = factory.Faker("md5")
    public_key = factory.Faker("sha256")

    class Meta:
        model = models.Delegate

    @factory.post_generation
    def histories(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for history in extracted:
                self.history.add(history)


class HistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.History


class NodeFactory(factory.django.DjangoModelFactory):
    delegate = factory.SubFactory(DelegateFactory)

    class Meta:
        model = models.Node


class ContributionFactory(factory.django.DjangoModelFactory):
    delegate = factory.SubFactory(DelegateFactory)
    title = factory.Faker("word")

    class Meta:
        model = models.Contribution
