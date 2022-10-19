import pytest

from core.models import Product


@pytest.mark.django_db
def test_create_order():
    p = Product.objects.create(name='test', hc_code=12121, etcng_code=343434, etcng_name='test etcng')
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_user_create1():
    count = Product.objects.all().count()
    assert count == 0
