import pytest


def test_counterparty(counterparty):
    assert counterparty.name == "Transcontainer"


def test_detail_counterparty(client, counterparty):
    response = client.get(f"/api/counterparty/counterparties/{counterparty.id}/")
    response.json()['name'] = counterparty.name
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_counterparty(client, counterparty):
    response = client.get("/api/counterparty/counterparties/")
    response.json()['name'] = counterparty.name
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_counterparty(client):
    response = client.post('/api/counterparty/counterparties/',
                           data={'name': 'Transgroup'})
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_counterparty(client, counterparty):
    response = client.put(f'/api/counterparty/counterparties/{counterparty.id}/',
                          data={'name': 'CMA'}, content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_counterparty(client, counterparty):
    response = client.delete(f'/api/counterparty/counterparties/{counterparty.id}/')
    assert response.status_code == 204
