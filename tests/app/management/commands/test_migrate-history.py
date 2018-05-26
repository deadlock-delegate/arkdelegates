import importlib

import pytest

from tests.app import factories


@pytest.mark.django_db
def test_command_correctly_populates_fk():
    module = importlib.import_module('app.management.commands.migrate-history')
    cmd = module.Command()

    history_a1 = factories.HistoryFactory()
    history_a2 = factories.HistoryFactory()
    delegate_a = factories.DelegateFactory(name='spongebob', histories=[history_a1, history_a2])

    history_b1 = factories.HistoryFactory()
    history_b2 = factories.HistoryFactory()
    delegate_b = factories.DelegateFactory(name='patrick', histories=[history_b1, history_b2])
    history_b2.delegate_fk = delegate_b
    history_b2.save()

    cmd.handle()

    history_a1.refresh_from_db()
    history_a2.refresh_from_db()
    assert history_a1.delegate_fk == delegate_a
    assert history_a2.delegate_fk == delegate_a

    history_b1.refresh_from_db()
    history_b2.refresh_from_db()
    assert history_b1.delegate_fk == delegate_b
    assert history_b2.delegate_fk == delegate_b
