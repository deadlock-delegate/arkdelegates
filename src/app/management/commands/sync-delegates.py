from django.core.management.base import BaseCommand
from django.db import transaction
import requests

from app.models import Delegate


class Command(BaseCommand):
    help = "Update delegates data"

    def handle(self, **options):
        self.stderr.write("Updating delegate stats")

        created_count = 0
        api_url = "http://159.89.109.90:4003"
        endpoint = "/api/v2/delegates?page=1&limit=100"

        while endpoint:
            url = f"{api_url}{endpoint}"
            self.stderr.write(f"... fetching 51 delegates from {url}")
            response = requests.get(url)
            if response.status_code != 200:
                self.stderr.write(
                    f"Request returned in invalid status code {response.status_code}. Quiting."
                )
                break

            json_dict = response.json()
            data = json_dict["data"]
            if not data:
                break

            with transaction.atomic():
                for delegate_data in data:
                    delegate, created = Delegate.objects.get_or_create(
                        name=delegate_data["username"],
                        address=delegate_data["address"],
                        public_key=delegate_data["publicKey"],
                    )
                    if created:
                        created_count += 1

            endpoint = json_dict["meta"]["next"]

        self.stderr.write(f"Created {created_count} new delegates")
