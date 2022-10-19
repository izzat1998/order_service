import pytest

from core.models import Product, Station


@pytest.fixture
def product(db):
    product = Product.objects.create(name='tea', hc_code=920000, etcng_code=9222, etcng_name='tea')
    return product


@pytest.fixture
def destination(db):
    destination = Station.objects.create(name='Chuqursay', code="720000", railway_name="Uzbekistan")
    return destination

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
