def test_preliminary_cost_create(client, container_type, counterparty_order):
    preliminary_cost_data = {
        'preliminary_cost': 12012,
        'counterparty_id': counterparty_order.id,
        'container_type_id': container_type.id

    }

    response = client.post('/container_order/preliminary_cost/create/', data=preliminary_cost_data,
                           content_type='application/json')
    assert response.status_code == 201


def test_preliminary_cost_update(client, preliminary_cost, container_type, counterparty_order):
    preliminary_cost_data = {
        'preliminary_cost': 1000
    }

    response = client.put(f'/container_order/preliminary_cost/update/{preliminary_cost.id}/',
                          data=preliminary_cost_data,
                          content_type='application/json')
    assert response.status_code == 200
    assert response.json()['preliminary_cost'] == '1000.00'


def test_preliminary_cost_delete(client, preliminary_cost):
    response = client.delete(f'/container_order/preliminary_cost/delete/{preliminary_cost.id}/',
                             content_type='application/json')
    assert response.status_code == 204
