from django.core.management.base import BaseCommand

from app.models import History


class Command(BaseCommand):
    help = 'Migrate history from ManyToMany to ForeignKey on Delegate'

    def handle(self, **options):
        histories = History.objects.filter(delegate_fk__isnull=True)

        self.stdout.write('No. of histories to update: {}'.format(histories.count()))
        for index, history in enumerate(histories):
            if index != 0 and index % 100 == 0:
                self.stdout.write(f'Updated delegate_fk of {index} histories. Still working...')

            delegates = history.delegate.all()

            if delegates.count() > 1:
                raise Exception('History is broken. Unbreak history, then run again.')

            history.delegate_fk = delegates.first()
            history.save()

        self.stdout.write('Done updating all deleagte_fk fields on all histories.')
