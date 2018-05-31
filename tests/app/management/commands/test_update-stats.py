import importlib

import pytest

import responses

from app.models import Delegate

from tests.app import factories


delegates_get_response = {
    'success': True,
    'delegate': {
        'username': 'deadlock',
        'address': 'AcNiPbV1XZ7wkFwoBD3NjpSGFEkyohYLER',
        'publicKey': 'spongebob',
        'vote': '142697747126082',
        'producedblocks': 2030,
        'missedblocks': 1,
        'rate': 34,
        'approval': 1.06,
        'productivity': 99.95
    }
}


delegates_voters_response = {
    'success': True,
    'accounts': [
        {
            'username': None,
            'address': 'AUpHeK8qNEWTegaYkQoX3e3rv3vda8Amas',
            'publicKey': 'patrick',
            'balance': '96510006839'
        },
    ]
}


@responses.activate
@pytest.mark.django_db
def test_update_stats_populates_delegate_fk_field_and_also_adds_it_as_manytomany():
    module = importlib.import_module('app.management.commands.update-stats')
    cmd = module.Command()

    delegate = factories.DelegateFactory(public_key='spongebob')

    responses.add(
        responses.GET,
        'https://explorer.ark.io:8443/api/delegates/get?publicKey={}'.format(delegate.public_key),
        json=delegates_get_response,
        status=200)

    responses.add(
        responses.GET,
        f'https://explorer.ark.io:8443/api/delegates/voters?publicKey={delegate.public_key}',
        json=delegates_voters_response,
        status=200)

    cmd.handle()

    delegates = Delegate.objects.all()
    assert delegates.count() == 1

    delegate = delegates.first()
    histories = delegate.history.all()
    assert histories.count() == 1

    history = histories.first()
    assert history.delegate_fk == delegate
