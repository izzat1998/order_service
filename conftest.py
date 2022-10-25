import datetime

import pytest

from container_order.models import CounterPartyOrder, ContainerOrder, ContainerTypeOrder, ContainerPreliminaryCost
from core.models import Product, Station
from counterparty.models import CounterpartyCategory, Counterparty
from order.models import Order


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


@pytest.fixture
def container_order(db, departure, destination, product, counterparty, category):
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
    counterparty_order = CounterPartyOrder.objects.create(counterparty=counterparty, category=category, order=order)
    container_order = ContainerOrder.objects.create(order=order, product=product,
                                                    sending_type=ContainerOrder.SENDING_TYPE_CHOICES[0][0])
    container_type = ContainerTypeOrder.objects.create(agreed_rate="1010.15", quantity=55, container_type='40HC',
                                                       order=container_order)

    ContainerPreliminaryCost.objects.create(counterparty=counterparty_order,
                                            container_type=container_type,
                                            preliminary_cost='125.45'
                                            )

    return container_order
