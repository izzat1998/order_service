import pytest


def test_product(product):
    assert product.name == "tea"


def test_detail_product(client, product):
    response = client.get(f"/api/core/products/{product.id}/")
    response.json()['name'] = product.name
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_product(client, product):
    response = client.get("/api/core/products/")
    response.json()['name'] = product.name
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_product(client):
    response = client.post('/api/core/products/',
                           data={'name': 'name_test', 'hc_code': 921000, 'etcng_code': 760000,
                                 'etcng_name': 'etcng_name'})
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_product(client, product):
    response = client.put(f'/api/core/products/{product.id}/',
                          data={'name': 'name_test22', 'hc_code': 921000, 'etcng_code': 760000,
                                'etcng_name': 'etcng_name'}, content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_product(client, product):
    response = client.delete(f'/api/core/products/{product.id}/')
    assert response.status_code == 204
