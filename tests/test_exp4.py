import pytest

from core.models import Product


def test_product(product):
    product = product
    assert product.name == "tea"


def test_destination(destination):
    assert destination.name == "Chuqursay"
