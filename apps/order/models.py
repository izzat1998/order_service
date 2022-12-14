from django.db import models

from apps.core.models import TimeStampedModel, Station, Product


class Order(TimeStampedModel):
    ORDER_TYPE_CHOICES = (
        ("import", "Import"),
        ("export", "Export"),
        ("transit", "Transit"),
    )

    SHIPMENT_STATUS_CHOICES = (
        ("in_process", "In process"),
        ("delivered", "Delivered"),
        ("completed", "Completed"),
    )
    PAYMENT_STATUS_CHOICES = (
        ("reserved", "Reserved"),
        ("issued", "Issued"),
        ("received", "Received"),
    )
    POSITION_CHOICES = (
        ("rail_forwarder", "Rail forwarder"),
        ("block_train", "Block train"),
        ("multi_modal", "Multi modal"),
    )
    order_number = models.PositiveIntegerField(null=True, unique=True)
    lot_number = models.CharField(blank=True, null=True, max_length=255)
    date = models.DateField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, choices=POSITION_CHOICES)
    # STATUSES
    type = models.CharField(
        max_length=50, choices=ORDER_TYPE_CHOICES, default=ORDER_TYPE_CHOICES[0][0]
    )

    shipment_status = models.CharField(
        max_length=50,
        choices=SHIPMENT_STATUS_CHOICES,
        default=SHIPMENT_STATUS_CHOICES[0][0],
    )
    payment_status = models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_STATUS_CHOICES[0][0],
    )
    # Order Detail
    shipper = models.CharField(max_length=255, blank=True, null=True)
    consignee = models.CharField(max_length=255, blank=True, null=True)
    departure = models.ForeignKey(
        Station, on_delete=models.SET_NULL, related_name="destination_orders", null=True
    )
    destination = models.ForeignKey(
        Station, on_delete=models.SET_NULL, related_name="departure_orders", null=True
    )
    border_crossing = models.CharField(max_length=255, blank=True, null=True)
    conditions_of_carriage = models.CharField(max_length=255, blank=True, null=True)
    rolling_stock = models.CharField(max_length=255, blank=True, null=True)
    departure_country = models.CharField(max_length=255, blank=True, null=True)
    destination_country = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    # USER
    manager = models.IntegerField(blank=True)
    customer = models.IntegerField(blank=True)
    request_file = models.FileField(upload_to="applications/", blank=True, null=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return str(self.order_number)

    @classmethod
    def last_number(cls):
        return cls.objects.last().order_number

    @classmethod
    def position_count(cls, position_type):
        return cls.objects.filter(position=position_type).count()

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class WagonOrder(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="wagon_order"
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, related_name="wagon_order", null=True
    )
    weight = models.IntegerField(default=60)
    quantity = models.IntegerField(default=0)

    class Meta:
        db_table = "wagon_order"
        verbose_name = "Wagon order"
        verbose_name_plural = "Wagon orders"

    def __str__(self):
        return str(self.order)

    def save(self, *args, **kwargs):
        if not hasattr(self.order, "container_order") and not hasattr(
                self.order, "empty_wagon_order"
        ):
            super(WagonOrder, self).save(*args, **kwargs)
        else:
            raise Exception("Order associated by order type or empty wagon type")


class WagonEmptyOrder(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="empty_wagon_order"
    )
    quantity = models.IntegerField(default=1)
    agreed_rate = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "wagon_empty_order"
        verbose_name = "Wagon empty order"
        verbose_name_plural = "Wagon empty orders"

    def __str__(self):
        return str(self.order)

    def save(self, *args, **kwargs):
        if not hasattr(self.order, "container_order") and not hasattr(
                self.order, "wagon_order"
        ):
            super(WagonEmptyOrder, self).save(*args, **kwargs)
        else:
            raise Exception("Order associated by order type or  wagon type")
