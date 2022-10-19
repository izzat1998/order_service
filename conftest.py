import datetime

import pytest

from core.models import Product, Station
from order.models import ContainerOrder, Order


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
def container_order(db, departure, destination, product):
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
    container_order = ContainerOrder.objects.create(order=order, product=product,
                                                    sending_type=ContainerOrder.SENDING_TYPE_CHOICES[0][0])
    return container_order
# @pytest.fixture
# def user_1(db):
#     product = Product.objects.create(name='product', hc_code=121313, etcng_code=12112, etcng_name='hello')
#     print('create-product')
#     return product
#
#
# @pytest.fixture
# def new_product_factory(db):
#     def create_product(
#             name: str,
#             hc_code: int,
#             etcng_code: int,
#             etcng_name: str
#     ):
#         product = Product.objects.create(name=name, hc_code=hc_code, etcng_code=etcng_code, etcng_name=etcng_name)
#         return product
#
#     return create_product


# @pytest.fixture
# def new_product(db, new_product_factory):
#     return new_product_factory("product", 12334, 12112, "hello")
