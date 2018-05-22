from django.core.management.base import BaseCommand
from django.db import transaction

import requests

from app.models import Delegate, History


class Command(BaseCommand):
    help = 'Update delegates data'

    def handle(self, **options):
        self.stderr.write('Updating delegates data')

        created_count = 0
        delegate_url = 'https://explorer.ark.io:8443/api/delegates/get?publicKey={}'
        voters_url = 'https://explorer.ark.io:8443/api/delegates/voters?publicKey={}'

        to_update = Delegate.objects.all()
        for delegate in to_update:
            delegate_response = requests.get(delegate_url.format(delegate.public_key))
            voters_response = requests.get(voters_url.format(delegate.public_key))
            if delegate_response.status_code != 200 or voters_response.status_code != 200:
                continue

            delegate_data = delegate_response.json()
            voters_data = voters_response.json()

            voting_power, voters_zero_balance = get_voting_stats(voters_data['accounts'])

            voters = len(voters_data['accounts'])
            with transaction.atomic():
                delegate_data = delegate_data.get('delegate')
                if delegate_data:
                    old_rank = delegate.history.last().rank
                    rank = delegate_data['rate']
                    rank_changed = old_rank - rank
                    history = History.objects.create(
                        voters=voters,
                        voting_power=voting_power,
                        uptime=delegate_data['productivity'],
                        approval=delegate_data['approval'],
                        rank=delegate_data['rate'],
                        rank_changed=rank_changed,
                        forged=delegate_data['producedblocks'],
                        missed=delegate_data['missedblocks'],
                        payload={
                            'voters_zero_balance': voters_zero_balance,
                            'voters_not_zero_balance': voters - voters_zero_balance,
                        }
                    )
                else:
                    self.stderr.write(f'Was not able to get delegate data for {delegate.name}')
                    history = History.objects.create(
                        voters=voters,
                        voting_power=voting_power,
                        payload={
                            'voters_zero_balance': voters_zero_balance,
                            'voters_not_zero_balance': voters - voters_zero_balance,
                        }
                    )
                delegate.history.add(history)

            created_count += 1

        self.stderr.write(f'Updated stats of {created_count} delegates')


def get_voting_stats(accounts):
    voting_power = 0
    voters_zero_balance = 0
    for voter in accounts:
        if voter['balance'] == '0':
            voters_zero_balance += 1
        voting_power += int(voter['balance'])
    return str(voting_power), voters_zero_balance
