import datetime

import pytest




@pytest.mark.django_db
def test_list_container_order(client, container_order):
    response = client.get('/api/container_order/list/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_container_order(client, container_order):
    response = client.get(f'/api/container_order/list/{container_order.order.order_number}/')
    assert response.json()[0]['order']['order_number'] == container_order.order.order_number
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_container_order(client, departure, destination, product, category, counterparty):
    order_json = {
        "order": {
            "order_number": 122,
            "lot_number": "1111",
            "date": "2022-10-14",
            "position": "Block train",
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
        "sending_type": "single",
        "product_id": product.id,
        "container_types": [
            {
                "agreed_rate": "500.00",
                "quantity": 35,
                "container_type": "40HC",
                "container_preliminary_costs": [
                    {
                        "category_id": category.id,
                        "counterparty_id": counterparty.id,
                        "preliminary_cost": "1500.00"

                    },
                ]
            }
        ]
    }
    response = client.post('/api/container_order/create/', data=order_json, content_type='application/json')

    assert response.status_code == 201


def test_update_container_order(client, container_order, departure, destination, product, category, counterparty):
    updated_order_json = {
        "order": {
            "order_number": 100,
            "lot_number": "1111",
            "date": "2022-10-14",
            "position": "Block train",
            "type": "import",
            "shipment_status": "delivered",
            "payment_status": "issued",
            "shipper": "LLC \"Gallaorol kaliy fosfat\"",
            "consignee": "How are you",
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
                    "id": container_order.order.counterparties.all()[0].id,
                    "category_id": category.id,
                    "counterparty_id": counterparty.id
                }

            ]
        },
        "sending_type": "single",
        "product_id": product.id,

        "container_types": [
            {
                "id": container_order.container_types.all()[0].id,
                "agreed_rate": "7711.00",
                "quantity": 10,
                "container_type": "20HC",
                "container_preliminary_costs": [
                    {"id": "3",
                     "preliminary_cost": "1500.00"
                     }
                ]
            }
        ]
    }

    response = client.put(f'/api/container_order/list/{container_order.order.order_number}/edit/',
                          data=updated_order_json,
                          content_type='application/json')

    assert response.status_code == 200


def test_delete_container_order(client, container_order):
    response = client.delete(f'/api/container_order/list/{container_order.order.order_number}/delete/',
                             content_type='application/json')

    assert response.status_code == 204
