import pytest


def test_territory(territory):
    assert territory.name == "UZB"


def test_detail_territory(client, territory):
    response = client.get(f"/core/territories/{territory.id}/")
    response.json()['name'] = territory.name
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_territory(client, territory):
    response = client.get("/core/territories/")
    response.json()['name'] = territory.name
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_territory(client):
    response = client.post('/core/territories/',
                           data={'name': 'RJD'})
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_territory(client, territory):
    response = client.put(f'/core/territories/{territory.id}/',
                          data={'name': 'TDJ'}, content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_territory(client, territory):
    response = client.delete(f'/core/territories/{territory.id}/')
    assert response.status_code == 204
