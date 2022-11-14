import pytest


def test_destination(destination):
    assert destination.name == "Altynkol"


def test_departure(departure):
    assert departure.name == "Chuqursay"


@pytest.mark.django_db
def test_detail_station(client, departure):
    response = client.get(f"/core/stations/{departure.id}/")
    response.json()['name'] = departure.name
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_station(client, product, departure, destination):
    response = client.get("/core/stations/")
    assert response.json()['count'] == 2
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_station(client):
    response = client.post('/core/stations/',
                           data={'name': 'station', 'code': "7200001", 'railway_name': "Uzbekistan"})
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_station(client, destination):
    response = client.put(f'/core/stations/{destination.id}/',
                          data={'name': 'station2', 'code': "7200001312"},
                          content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_station(client, destination):
    response = client.delete(f'/core/stations/{destination.id}/')
    assert response.status_code == 204
