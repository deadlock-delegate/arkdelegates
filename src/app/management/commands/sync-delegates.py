import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import Delegate


class Command(BaseCommand):
    help = 'Update delegates data'

    def handle(self, **options):
        self.stderr.write('Updating delegate stats')

        created_count = 0
        offset = 0
        limit = 51
        url = 'https://explorer.ark.io:8443/api/delegates?orderBy=rate:asc&offset={}&limit={}'

        while True:
            self.stderr.write(f'... fetching 51 delegates from {url.format(offset, limit)}')
            response = requests.get(url.format(offset, limit))
            if response.status_code != 200:
                self.stderr.write(
                    f'Request returned in invalid status code {response.status_code}. Quiting.'
                )
                break

            data = response.json()
            if not data['delegates']:
                break

            with transaction.atomic():
                for delegate_data in data['delegates']:
                    delegate, created = Delegate.objects.get_or_create(
                        name=delegate_data['username'],
                        address=delegate_data['address'],
                        public_key=delegate_data['publicKey']
                    )
                    if created:
                        created_count += 1

            offset += limit

        self.stderr.write(f'Created {created_count} new delegates')
