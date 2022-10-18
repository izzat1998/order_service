from enum import unique

from django.db import models

from core.models import TimeStampedModel, Station, Product
from counterparty.models import Counterparty, Category


class Order(TimeStampedModel):
    ORDER_TYPE_CHOICES = (
        ('import', 'Import'),
        ('export', 'Export'),
        ('transit', 'Transit'),
    )

    SHIPMENT_STATUS_CHOICES = (
        ('in_process', 'In process'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed')
    )
    PAYMENT_STATUS_CHOICES = (
        ('reserved', 'Reserved'),
        ('issued', 'Issued'),
        ('received', 'Received'),
    )
    POSITION_CHOICES = (
        ('Rail forwarder', 'Rail forwarder'),
        ('Block train', 'Block train'),
        ('Multi modal', 'Multi modal'),
    )
    order_number = models.PositiveIntegerField(null=True, unique=True)
    lot_number = models.CharField(blank=True, null=True, max_length=255)
    date = models.DateField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, choices=POSITION_CHOICES)
    # STATUSES
    type = models.CharField(max_length=50, choices=ORDER_TYPE_CHOICES, default=ORDER_TYPE_CHOICES[0][0])

    shipment_status = models.CharField(max_length=50, choices=SHIPMENT_STATUS_CHOICES,
                                       default=SHIPMENT_STATUS_CHOICES[0][0])
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES,
                                      default=PAYMENT_STATUS_CHOICES[0][0])
    # Order Detail
    shipper = models.CharField(max_length=255, blank=True, null=True)
    consignee = models.CharField(max_length=255, blank=True, null=True)
    departure = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='destination_orders', null=True)
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='departure_orders', null=True)
    border_crossing = models.CharField(max_length=255, blank=True, null=True)
    conditions_of_carriage = models.CharField(max_length=255, blank=True, null=True)
    rolling_stock = models.CharField(max_length=255, blank=True, null=True)
    departure_country = models.CharField(max_length=255, blank=True, null=True)
    destination_country = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    # USER
    manager = models.IntegerField(blank=True)
    customer = models.IntegerField(blank=True)
    request_file = models.FileField(upload_to='applications/', blank=True, null=True)

    def __str__(self):
        return str(self.order_number)

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class ContainerOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='container_order')
    SENDING_TYPE_CHOICES = (
        ('single', 'Single'),
        ('block_train', 'Block train')
    )
    sending_type = models.CharField(max_length=50, choices=SENDING_TYPE_CHOICES, default=SENDING_TYPE_CHOICES[0][0])
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='container_order', null=True)

    class Meta:
        db_table = 'container_order'
        verbose_name = 'Container order'
        verbose_name_plural = 'Container orders'

    def __str__(self):
        return str(self.order)

    def save(self, *args, **kwargs):
        if not hasattr(self.order, 'wagon_order') and not hasattr(self.order, 'empty_wagon_order'):
            super(ContainerOrder, self).save(*args, **kwargs)
        else:
            raise Exception('Order associated by wagon type')


class WagonOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='wagon_order')
    product = models.CharField(max_length=255, blank=True, null=True)
    gng = models.CharField(max_length=255, blank=True, null=True)
    etcng = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'wagon_order'
        verbose_name = 'Wagon order'
        verbose_name_plural = 'Wagon orders'

    def __str__(self):
        return str(self.order)

    def save(self, *args, **kwargs):
        if not hasattr(self.order, 'container_order') and not hasattr(self.order, 'empty_wagon_order'):
            super(WagonOrder, self).save(*args, **kwargs)
        else:
            raise Exception('Order associated by order type or empty wagon type')


class WagonEmptyOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='empty_wagon_order')

    class Meta:
        db_table = 'wagon_empty_order'
        verbose_name = 'Wagon empty order'
        verbose_name_plural = 'Wagon empty orders'

    def __str__(self):
        return str(self.order)

    def save(self, *args, **kwargs):
        if not hasattr(self.order, 'container_order') and not hasattr(self.order, 'wagon_order'):
            super(WagonEmptyOrder, self).save(*args, **kwargs)
        else:
            raise Exception('Order associated by order type or  wagon type')


class CounterPartyOrder(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='counterparties')
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('order', 'counterparty', 'category')
        db_table = 'counterparty_order'
        verbose_name = 'Counterparty order'
        verbose_name_plural = 'Counterparty orders'

    def __str__(self):
        return str(self.order) + '-' + str(self.counterparty) + '-' + str(self.category)


class ContainerTypeOrder(TimeStampedModel):
    CONTAINER_TYPE_CHOICES = (
        ('20', '20'),
        ('20HC', '20HC'),
        ('40', '40'),
        ('40HC', '40HC'),
        ('45', '45'),

    )
    agreed_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    container_type = models.CharField(max_length=100, choices=CONTAINER_TYPE_CHOICES)

    order = models.ForeignKey(ContainerOrder, related_name='container_types',
                              on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('container_type', 'order')
        db_table = 'container_type_order'
        verbose_name = 'ContainerType order'
        verbose_name_plural = 'ContainerType orders'

    def __str__(self):
        return str(self.order) + '-' + str(self.container_type)


class ContainerPreliminaryCost(TimeStampedModel):
    container_type = models.ForeignKey(ContainerTypeOrder, on_delete=models.CASCADE,
                                       related_name='container_preliminary_costs')
    counterparty = models.ForeignKey(CounterPartyOrder, on_delete=models.CASCADE,
                                     )
    preliminary_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        unique_together = ('container_type', 'counterparty')
        db_table = 'container_preliminary_cost'
        verbose_name = 'Container preliminary cost'
        verbose_name_plural = 'Container preliminary costs'

    def __str__(self):
        return str(self.container_type) + '-' + str(self.counterparty)


class Container(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'container'
        verbose_name = 'Container'
        verbose_name_plural = 'Containers'

    def __str__(self):
        return self.name


class ContainerExpanse(TimeStampedModel):
    counterparty = models.ForeignKey(CounterPartyOrder,  on_delete=models.CASCADE)
    container = models.ForeignKey(Container, on_delete=models.CASCADE)
    container_type = models.ForeignKey(ContainerTypeOrder,related_name='expanses', on_delete=models.CASCADE)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('counterparty', 'container')
        db_table = 'container_expanse'
        verbose_name = 'Container expanse'
        verbose_name_plural = 'Container expanses'

    def __str__(self):
        return str(self.container_type) + '-' + str(self.counterparty) + '-' + str(self.container)
