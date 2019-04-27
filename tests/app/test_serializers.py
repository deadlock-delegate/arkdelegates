from datetime import datetime
from decimal import Decimal

import pytest

from app.serializers import DelegateInfo

from tests.app import factories


@pytest.mark.django_db
def test_delegate_info_returns_correct_data():

    delegate = factories.DelegateFactory(
        name="spongebob",
        website="deadlock.sh",
        proposal="this is my proposal",
        is_private=False,
        payout_covering_fee=False,
        payout_percent=Decimal("90"),
        payout_interval=2,
        payout_minimum="0.03",
        payout_maximum="123",
        payout_minimum_vote_amount=None,
        payout_maximum_vote_amount=None,
    )

    factories.HistoryFactory(delegate_fk=delegate, created=datetime(2018, 5, 25))
    history = factories.HistoryFactory(
        delegate_fk=delegate,
        voters=10,
        approval=1.07,
        rank=32,
        forged=3331.0,
        voting_power="143321527262092",
        payload={"voters_zero_balance": 3, "voters_not_zero_balance": 10},
        created=datetime.now(),
    )

    delegate_b = factories.DelegateFactory(name="patrick")
    factories.HistoryFactory(delegate_fk=delegate_b, voters=1337, rank=2, created=datetime.now())

    factories.NodeFactory(delegate=delegate, is_active=True)
    factories.NodeFactory(delegate=delegate, is_active=True, is_backup=True)
    factories.NodeFactory(delegate=delegate, is_active=False, is_backup=True)

    factories.ContributionFactory(delegate=delegate)

    info = DelegateInfo.from_slug("spongebob").data

    assert info["id"] == delegate.id
    assert info["name"] == delegate.name
    assert info["slug"] == delegate.slug
    assert info["address"] == delegate.address
    assert info["public_key"] == delegate.public_key
    assert info["website"] == delegate.website
    assert info["proposal"] == delegate.proposal
    assert info["is_private"] == delegate.is_private
    assert info["payout_covering_fee"] == delegate.payout_covering_fee
    assert info["payout_percent"] == delegate.payout_percent
    assert info["payout_interval"] == delegate.payout_interval
    assert info["payout_minimum"] == delegate.payout_minimum
    assert info["payout_maximum"] == delegate.payout_maximum
    assert info["payout_minimum_vote_amount"] == delegate.payout_minimum_vote_amount
    assert info["payout_maximum_vote_amount"] == delegate.payout_maximum_vote_amount
    assert info["user_id"] == delegate.user_id
    assert "created" in info
    assert "updated" in info

    assert info["approval"] == history.approval
    assert info["rank"] == history.rank
    assert info["forged"] == history.forged
    assert info["voters"] == history.voters
    assert info["voting_power"] == history.voting_power
    assert info["voters_zero_balance"] == history.payload["voters_zero_balance"]
    assert info["voters_not_zero_balance"] == history.payload["voters_not_zero_balance"]

    assert info["total_nodes_count"] == 2
    assert info["backup_nodes_count"] == 1
    assert info["contributions_count"] == 1
