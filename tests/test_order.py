import datetime

import pytest

from order.models import Order, ContainerOrder


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
    response = client.post('/api/order/create/', data=order_json, content_type='application/json')

    assert response.status_code == 201
