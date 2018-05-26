from datetime import datetime

import pytest

from app.views.delegate import DelegateView

from tests.app import factories


@pytest.mark.django_db
def test_fetch_delegate_info_returns_correct_delegate_with_history():
    history_a1 = factories.HistoryFactory(voters=123, rank=1, created=datetime(2018, 5, 25))
    history_a2 = factories.HistoryFactory(voters=456, rank=3, created=datetime.now())
    delegate_a = factories.DelegateFactory(name='spongebob', histories=[history_a1, history_a2])

    history_b = factories.HistoryFactory(voters=1337, rank=2, created=datetime.now())
    factories.DelegateFactory(name='patrick', histories=[history_b])
    delegate = DelegateView()._fetch_delegate_info('spongebob')

    assert delegate.id == delegate_a.id
    assert delegate.name == delegate_a.name
    assert delegate.address == delegate_a.address
    assert delegate.voters == 456
    assert delegate.uptime is None
    assert delegate.approval is None
    assert delegate.rank == 3
    assert delegate.forged is None
    assert delegate.missed is None
    assert delegate.voting_power is None
    assert delegate.voters_zero_balance is None
    assert delegate.voters_not_zero_balance is None
