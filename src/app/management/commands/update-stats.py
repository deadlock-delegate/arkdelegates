from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
import requests

from app.models import Delegate, History


API_URL = "http://159.89.109.90:4003"


class Command(BaseCommand):
    help = "Update delegates data"

    def handle(self, **options):
        self.stdout.write("Updating delegates data")

        created_count = 0

        to_update = Delegate.objects.all()
        for delegate in to_update:
            self.stderr.write(f"Syncing data for {delegate.name}")
            public_key = delegate.public_key

            response = requests.get(f"{API_URL}/api/v2/delegates/{public_key}")
            json_dict = response.json()
            data = json_dict["data"]

            voters, voting_power, voters_zero_balance = get_voting_stats_for_delegate(public_key)

            with transaction.atomic():
                rank = data["rank"]
                if data:
                    rank_changed = 0
                    rank_history = delegate.history.filter(
                        created__gt=datetime.now() - timedelta(hours=25),
                        created__lt=datetime.now() - timedelta(hours=23),
                    ).last()

                    if rank_history:
                        old_rank = rank_history.rank
                        rank_changed = old_rank - rank

                    history = History.objects.create(
                        delegate_fk=delegate,
                        voters=voters,
                        voting_power=voting_power,
                        approval=data["production"]["approval"],
                        rank=rank,
                        rank_changed=rank_changed,
                        forged=data["blocks"]["produced"],
                        payload={
                            "voters_zero_balance": voters_zero_balance,
                            "voters_not_zero_balance": voters - voters_zero_balance,
                        },
                    )
                else:
                    self.stderr.write(f"Was not able to get delegate data for {delegate.name}")
                    history = History.objects.create(
                        delegate_fk=delegate,
                        voters=voters,
                        voting_power=voting_power,
                        payload={
                            "voters_zero_balance": voters_zero_balance,
                            "voters_not_zero_balance": voters - voters_zero_balance,
                        },
                    )
                delegate.history.add(history)

            created_count += 1

        self.stdout.write(f"Updated stats of {created_count} delegates")


def get_voting_stats_for_delegate(public_key):
    voting_power = 0
    voters_zero_balance = 0
    voters_count = 0
    endpoint = f"/api/v2/delegates/{public_key}/voters"

    while endpoint:
        response = requests.get(f"{API_URL}{endpoint}")
        json_dict = response.json()
        for voter in json_dict["data"]:
            if not voter["balance"]:
                voters_zero_balance += 1
            voting_power += int(voter["balance"])
            voters_count += 1

        endpoint = json_dict["meta"]["next"]

    return voters_count, str(voting_power), voters_zero_balance
