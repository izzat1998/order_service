def test_container_type_create(client, container_order):
    type_data = {
        'agreed_rate': 24000,
        'quantity': 50,
        'container_type': '40HC',
        'order_number': container_order.order.order_number
    }
    response = client.post('/container_order/container_type/create/', data=type_data, content_type='application/json')
    assert response.status_code == 201


def test_container_type_update(client, container_type):
    type_data = {
        'agreed_rate': 24000,
        'quantity': 50,
        'container_type': '40HC',
    }
    response = client.put(f'/container_order/container_type/update/{container_type.id}/', data=type_data,
                          content_type='application/json')
    assert response.status_code == 200


def test_container_type_delete(client, container_type):
    response = client.delete(f'/container_order/container_type/delete/{container_type.id}/',
                             content_type='application/json')
    assert response.status_code == 204
