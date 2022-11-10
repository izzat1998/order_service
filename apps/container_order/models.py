from django.db import models

from apps.core.models import TimeStampedModel, Product, Container
from apps.counterparty.models import Counterparty, CounterpartyCategory
from apps.order.models import Order


# Create your models here.
class ContainerOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='container_order')
    SENDING_TYPE_CHOICES = (
        ('single', 'Single'),
        ('block_train', 'Block train')
    )
    sending_type = models.CharField(max_length=50, choices=SENDING_TYPE_CHOICES, default=SENDING_TYPE_CHOICES[0][0])
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='container_order', null=True)

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


class CounterPartyOrder(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='counterparties')
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE)
    category = models.ForeignKey(CounterpartyCategory, on_delete=models.CASCADE, related_name='counterparty_orders')

    class Meta:
        ordering = ['id']
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


class ContainerActualCost(TimeStampedModel):
    counterparty = models.ForeignKey(CounterPartyOrder, on_delete=models.CASCADE)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    container_expanse = models.ForeignKey('ContainerExpanse', related_name='actual_costs', on_delete=models.CASCADE,
                                          null=True)

    class Meta:
        ordering = ['counterparty']
        unique_together = ('counterparty', 'container_expanse')


class ContainerExpanse(TimeStampedModel):
    container = models.ForeignKey(Container, on_delete=models.CASCADE, null=True, blank=True)
    container_type = models.ForeignKey(ContainerTypeOrder, related_name='expanses', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('container_type', 'container')
        db_table = 'container_expanse'
        verbose_name = 'Container expanse'
        verbose_name_plural = 'Container expanses'

    def __str__(self):
        return str(self.container_type) + '-' + '-' + str(self.container)
