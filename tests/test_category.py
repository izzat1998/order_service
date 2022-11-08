import pytest


def test_category(category):
    assert category.name == "Rail freight"


def test_detail_category(client, category):
    response = client.get(f"/counterparty/categories/{category.id}/")
    response.json()['name'] = category.name
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_category(client, category):
    response = client.get("/counterparty/categories/")
    response.json()['name'] = category.name
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_category(client):
    response = client.post('/counterparty/categories/',
                           data={'name': 'Ocean freight'})
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_category(client, category):
    response = client.put(f'/counterparty/categories/{category.id}/',
                          data={'name': 'Rail'}, content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_category(client, category):
    response = client.delete(f'/counterparty/categories/{category.id}/')
    assert response.status_code == 204
