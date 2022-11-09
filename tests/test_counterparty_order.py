import pytest


@pytest.mark.django_db
def test_list_counterparty_order(client, counterparty_order2):
    response = client.get(f'/order/counterparty/list/', content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_counterparty_order(client, counterparty_order2, counterparty_2, category_2):
    counterparty_order_data = {
        "counterparty_id": counterparty_2.id,
        "category_id": category_2.id,
    }

    response = client.put(f'/order/counterparty/update/{counterparty_order2.id}/',
                          data=counterparty_order_data,
                          content_type='application/json')

    assert response.status_code == 200


@pytest.mark.django_db
def test_create_counterparty_order(client, container_order, counterparty_2, category_2):
    counterparty_order = {
        "order_number": container_order.order.order_number,
        "counterparty_id": counterparty_2.id,
        "category_id": category_2.id,

    }
    response = client.post('/order/counterparty/create/', data=counterparty_order,
                           content_type='application/json')

    assert response.status_code == 201


@pytest.mark.django_db
def test_delete_counterparty_order(client, counterparty_order2):
    response = client.delete(f'/order/counterparty/delete/{counterparty_order2.id}/',
                             content_type='application/json')

    assert response.status_code == 204
