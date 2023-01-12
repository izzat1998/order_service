import datetime

import pytest


@pytest.mark.django_db
def test_list_container_order(client, container_order):
    response = client.get('/container_order/list/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_container_order(client, container_order):
    response = client.get(f'/container_order/list/{container_order.order.order_number}/')
    assert response.json()[0]['order']['order_number'] == container_order.order.order_number
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_container_order(client, departure, destination, product, category, counterparty):
    order_json = {
        "order": {
            "lot_number": "1111",
            "date": "2022-10-14",
            "position": "block_train",
            "type": "import",
            "shipment_status": "delivered",
            "payment_status": "issued",
            "shipper": "LLC \"Gallaorol kaliy fosfat\"",
            "consignee": "FE MEDEX",
            "departure_id": departure.id,
            "destination_id": destination.id,
            "border_crossing": "Келес эксп - Сарыагач эксп",
            "conditions_of_carriage": "FOB-FOR",
            "rolling_stock": "СПС контейнер",
            "departure_country": "Uzbekistan",
            "destination_country": "China",
            "comment": "Hello world",
            "manager": 1,
            "customer": 1,
            "counterparties": [
                {
                    "category_id": category.id,
                    "counterparty_id": counterparty.id
                }
            ]
        },
        "container_types": [
            {
                "agreed_rate": "2500.00",
                "quantity": 10,
                "container_type": "20HC",
                "container_preliminary_costs": [
                    {
                        "category_id": category.id,
                        "counterparty_id": counterparty.id,
                        "preliminary_cost": "2200.00"

                    }
                ]
            },
            {
                "agreed_rate": "3500.00",
                "quantity": 10,
                "container_type": "40HC",
                "container_preliminary_costs": [
                    {
                        "category_id": category.id,
                        "counterparty_id": counterparty.id,
                        "preliminary_cost": "3200.00"

                    }
                ]
            }
        ],
        "sending_type": "single",
        "product_id": product.id
    }
    response = client.post('/container_order/create/', data=order_json, content_type='application/json')

    assert response.status_code == 201


def test_update_container_order(client, container_order, departure, destination, product, category, counterparty):
    updated_order_json = {
        "order": {
            "order_number": 665,
            "lot_number": "1111",
            "date": "2022-10-14",
            "position": "block_train",
            "type": "import",
            "shipment_status": "delivered",
            "payment_status": "issued",
            "shipper": "LLC \"Gallaorol kaliy fosfat\"",
            "consignee": "FE MEDEX",
            "departure_id": departure.id,
            "destination_id": destination.id,
            "border_crossing": "Келес эксп - Сарыагач эксп",
            "conditions_of_carriage": "FOB-FOR",
            "rolling_stock": "СПС контейнер",
            "departure_country": "Uzbekistan",
            "destination_country": "China",
            "comment": "Hello world",
            "manager": 1,
            "customer": 1
        },
        "sending_type": "single",
        "product_id": product.id
    }

    response = client.put(f'/container_order/list/{container_order.order.order_number}/edit/',
                          data=updated_order_json,
                          content_type='application/json')

    assert response.status_code == 200


def test_delete_container_order(client, container_order):
    response = client.delete(f'/container_order/list/{container_order.order.order_number}/delete/',
                             content_type='application/json')

    assert response.status_code == 204
