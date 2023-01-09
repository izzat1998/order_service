from django.db import models

from apps.core.models import TimeStampedModel, Station, Product, Territory
from apps.counterparty.models import Counterparty


class Application(TimeStampedModel):
    LOADING_CHOICES = (
        ("container", "Container"),
        ("wagon", "Wagon"),
        ("empty_wagon", "EmptyWagon"),
    )
    CONTAINER_TYPE = (
        ('20', '20'),
        ('20H', '20H'),
        ('40', '40'),
        ('40H', '40H'),
        ('45', '45'),
    )
    SENDING_TYPE = (
        ("Одиночная", "Одиночная"),
        ("КП", "КП"),
    )

    prefix = models.CharField(max_length=255)
    number = models.IntegerField()
    quantity = models.IntegerField(default=1)
    date = models.DateField(blank=True, null=True)
    period = models.CharField(max_length=50, blank=True, null=True)
    sending_type = models.CharField(choices=SENDING_TYPE, default=SENDING_TYPE[0][0], max_length=50)
    shipper = models.CharField(max_length=255, blank=True, null=True)
    consignee = models.CharField(max_length=255, blank=True, null=True)
    condition_of_carriage = models.CharField(max_length=255, blank=True, null=True)
    agreed_rate = models.CharField(max_length=255, blank=True, null=True)
    border_crossing = models.CharField(max_length=255, blank=True, null=True)
    departure_country = models.CharField(max_length=255, blank=True, null=True)
    destination_country = models.CharField(max_length=255, blank=True, null=True)
    departure = models.ForeignKey(Station, related_name='departure_applications', on_delete=models.SET_NULL
                                  , null=True)
    destination = models.ForeignKey(Station, related_name='destination_applications', on_delete=models.SET_NULL,
                                    null=True)
    rolling_stock_1 = models.CharField(max_length=255, blank=True, null=True)
    rolling_stock_2 = models.CharField(max_length=255, blank=True, null=True)
    paid_telegram = models.CharField(max_length=255, blank=True, null=True)
    containers_or_wagons = models.TextField(blank=True, null=True, max_length=255)
    product = models.ForeignKey(Product, related_name='product_applications', on_delete=models.SET_NULL, null=True)
    loading_type = models.CharField(
        max_length=50,
        choices=LOADING_CHOICES,
        default=LOADING_CHOICES[0][0],
    )
    container_type = models.CharField(max_length=50, choices=CONTAINER_TYPE, null=True, blank=True)
    weight = models.CharField(max_length=50, blank=True, null=True)
    territories = models.ManyToManyField(Territory, related_name='applications')

    forwarder = models.ForeignKey(Counterparty, related_name='applications', on_delete=models.SET_NULL, null=True)
    manager = models.IntegerField(blank=True)
    customer = models.IntegerField(blank=True)
    file = models.FileField('applications/', null=True)

    def __str__(self):
        return self.prefix + str(self.number)

    @classmethod
    def last_number(cls):
        return cls.objects.last().number if cls.objects.count() > 0 else 0

    class Meta:
        ordering = ('number',)
        db_table = "application"
        verbose_name = "Application"
        verbose_name_plural = "Applications"
