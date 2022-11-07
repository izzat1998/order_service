from django.db import models


# Create your models here.

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Station(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    railway_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "code"], name='station_constraint'),
        ]
        db_table = 'station'
        verbose_name = 'Station'
        verbose_name_plural = 'Stations'

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    name = models.TextField()
    hc_code = models.PositiveIntegerField(blank=True, null=True)
    etcng_code = models.PositiveIntegerField(null=True, blank=True)
    etcng_name = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "hc_code", "etcng_code", "etcng_name"], name='product_constraint'),
        ]
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'{self.name}({self.hc_code}, {self.etcng_code})'


class Container(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'container'
        verbose_name = 'Container'
        verbose_name_plural = 'Containers'

    def __str__(self):
        return self.name
