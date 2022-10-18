from django.db import models

from core.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = 'category'

    def __str__(self):
        return self.name


# Create your models here.
class Counterparty(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Counterparty"
        verbose_name_plural = "Counterparties"
        db_table = 'counterparty'

    def __str__(self):
        return self.name

