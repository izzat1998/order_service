import pytest


@pytest.mark.django_db
def test_create_container_order(client, container_order):
    order_json = {
        "counterparty_id": container_order.order.counterparties.all()[0].id,
        "container_type_id": container_order.container_types.all()[0].id,
        "actual_cost": 12.27,
        "containers": [
            {
                "container_name": "rrtrtrtrt",
                "actual_cost": 12.4
            },
            {
                "container_name": "23232",
                "actual_cost": 12.45
            },
            {
                "container_name": "SSLMU78ouikhjm7777",
                "actual_cost": 12.45
            },
            {
                "container_name": "ertrtf35",
                "actual_cost": 12.45
            }
        ]

    }
    response = client.post(f'/api/order/list/{container_order.order.order_number}/expanse/create/', data=order_json,
                           content_type='application/json')

    assert response.status_code == 201
