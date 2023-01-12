import datetime

import pytest

from apps.container_order.models import ContainerOrder, CounterPartyOrder, ContainerTypeOrder, ContainerPreliminaryCost
from apps.core.models import Product, Station, Territory
from apps.counterparty.models import CounterpartyCategory, Counterparty
from apps.order.models import Order


# Core
@pytest.fixture
def territory(db):
    return Territory.objects.create(name='UZB')


@pytest.fixture
def product(db):
    product = Product.objects.create(name='tea', hc_code=920000, etcng_code=9222, etcng_name='tea')
    return product


@pytest.fixture
def departure(db):
    destination = Station.objects.create(name='Chuqursay', code="720000", railway_name="Uzbekistan")
    return destination


@pytest.fixture
def destination(db):
    destination = Station.objects.create(name='Altynkol', code="720220", railway_name="Kazakhstan")
    return destination


@pytest.fixture
def category(db):
    category = CounterpartyCategory.objects.create(name='Rail freight')
    return category


@pytest.fixture
def counterparty(db):
    counterparty = Counterparty.objects.create(name='Transcontainer')
    return counterparty


# Container order

@pytest.fixture
def base_container_order(db, departure, destination):
    order = Order.objects.create(
        order_number=7777,
        lot_number="12345",
        date=datetime.date.today(),
        position=Order.POSITION_CHOICES[0][0],
        type=Order.ORDER_TYPE_CHOICES[0][0],
        shipment_status=Order.SHIPMENT_STATUS_CHOICES[0][0],
        payment_status=Order.PAYMENT_STATUS_CHOICES[0][0],
        shipper='shipper',
        consignee='consignee',
        departure=departure,
        destination=destination,
        border_crossing='border_crossing',
        conditions_of_carriage='FOR-FOR',
        rolling_stock='SPS',
        departure_country='Uzbekistan',
        destination_country='China',
        comment='This is our comment',
        manager=1,
        customer=1,

    )
    return order


@pytest.fixture
def container_order(db, base_container_order, product):
    container_order = ContainerOrder.objects.create(order=base_container_order, product=product,
                                                    sending_type=ContainerOrder.SENDING_TYPE_CHOICES[0][0])

    return container_order


@pytest.fixture
def container_type(db, container_order):
    return ContainerTypeOrder.objects.create(agreed_rate='123.12', quantity=10, container_type='40HC',
                                             order=container_order)


@pytest.fixture
def counterparty_order(base_container_order, counterparty, category):
    counterparty_order = CounterPartyOrder.objects.create(order=base_container_order, counterparty=counterparty,
                                                          category=category)
    return counterparty_order


@pytest.fixture
def preliminary_cost(container_type, counterparty_order):
    return ContainerPreliminaryCost.objects.create(container_type=container_type, counterparty=counterparty_order,
                                                   preliminary_cost='123.10')
