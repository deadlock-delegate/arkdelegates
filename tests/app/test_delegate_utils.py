from datetime import datetime

import pytest

from app.delegate_utils import fetch_delegates

from tests.app import factories


@pytest.mark.django_db
def test_fetch_delegates_list_returns_correct_delegates_for_no_search_query():
    delegate_a = factories.DelegateFactory(name='spongebob')
    factories.HistoryFactory(
        delegate_fk=delegate_a, voters=123, rank=1, created=datetime(2018, 5, 25))
    factories.HistoryFactory(
        delegate_fk=delegate_a, voters=456, rank=3, created=datetime.now())

    delegate_b = factories.DelegateFactory(name='patrick')
    factories.HistoryFactory(
        delegate_fk=delegate_b, voters=1337, rank=2, created=datetime.now())

    factories.NodeFactory(delegate=delegate_b, is_active=True)
    factories.NodeFactory(delegate=delegate_b, is_active=True, is_backup=True)
    factories.NodeFactory(delegate=delegate_b, is_active=False)

    factories.ContributionFactory(delegate=delegate_a)

    delegates_list, _ = fetch_delegates(0)

    assert [delegate_b.id, delegate_a.id] == [x['id'] for x in delegates_list]

    assert delegates_list[0]['total_nodes_count'] == 2
    assert delegates_list[0]['backup_nodes_count'] == 1
    assert delegates_list[0]['contributions_count'] is None

    assert delegates_list[1]['contributions_count'] == 1


@pytest.mark.django_db
def test_fetch_delegates_list_returns_correct_delegates_for_search_query():
    delegate_a = factories.DelegateFactory(name='spongebob')
    factories.HistoryFactory(
        delegate_fk=delegate_a, voters=123, rank=1, created=datetime(2018, 5, 25))
    factories.HistoryFactory(
        delegate_fk=delegate_a, voters=456, rank=3, created=datetime.now())

    delegate_b = factories.DelegateFactory(name='patrick')
    factories.HistoryFactory(delegate_fk=delegate_b, voters=1337, rank=2, created=datetime.now())

    factories.NodeFactory(delegate=delegate_b, is_active=True)
    factories.NodeFactory(delegate=delegate_b, is_active=True, is_backup=True)
    factories.NodeFactory(delegate=delegate_b, is_active=False)

    factories.ContributionFactory(delegate=delegate_a)

    delegates_list, _ = fetch_delegates(0, 'spongebob')

    assert [delegate_a.id] == [x['id'] for x in delegates_list]

    assert delegates_list[0]['total_nodes_count'] is None
    assert delegates_list[0]['backup_nodes_count'] is None
    assert delegates_list[0]['contributions_count'] == 1


@pytest.mark.parametrize('search_query', [
    '',
    'spongebob',
])
@pytest.mark.django_db
def test_fetch_delegates_list_returns_delegate_with_correct_fields(search_query):
    delegate = factories.DelegateFactory(name='spongebob')
    factories.HistoryFactory(
        delegate_fk=delegate, voters=123, rank=1, created=datetime(2018, 5, 25))
    factories.HistoryFactory(
        delegate_fk=delegate, voters=456, rank=3, created=datetime.now())

    factories.NodeFactory(delegate=delegate, is_active=True)
    factories.NodeFactory(delegate=delegate, is_active=True, is_backup=True)
    factories.NodeFactory(delegate=delegate, is_active=False)

    factories.ContributionFactory(delegate=delegate)

    delegates_list, _ = fetch_delegates(0, search_query)

    assert [delegate.id] == [x['id'] for x in delegates_list]

    assert delegates_list[0]['name'] == delegate.name
    assert delegates_list[0]['address'] == delegate.address
    assert delegates_list[0]['voters'] == 456
    assert delegates_list[0]['approval'] is None
    assert delegates_list[0]['rank'] == 3
    assert delegates_list[0]['forged'] is None
    assert delegates_list[0]['voting_power'] is None
    assert delegates_list[0]['voters_zero_balance'] is None
    assert delegates_list[0]['voters_not_zero_balance'] is None
    assert delegates_list[0]['total_nodes_count'] == 2
    assert delegates_list[0]['backup_nodes_count'] == 1
    assert delegates_list[0]['contributions_count'] == 1
