from django.db import models

from apps.container_order.models import CounterPartyOrder
from apps.core.models import TimeStampedModel, Wagon
from apps.order.models import WagonOrder, WagonEmptyOrder


class WagonEmptyPreliminaryCost(TimeStampedModel):
    order = models.ForeignKey(WagonEmptyOrder, on_delete=models.CASCADE,
                              related_name='wagon_empty_preliminary_costs')
    counterparty = models.ForeignKey(CounterPartyOrder, on_delete=models.CASCADE,
                                     )
    preliminary_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


class WagonEmptyActualCost(TimeStampedModel):
    counterparty = models.ForeignKey(CounterPartyOrder, on_delete=models.CASCADE)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    wagon_expanse = models.ForeignKey('WagonEmptyExpanse', related_name='actual_costs', on_delete=models.CASCADE,
                                      null=True)

    class Meta:
        unique_together = ('counterparty', 'wagon_expanse')


class WagonEmptyExpanse(models.Model):
    agreed_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order = models.ForeignKey(WagonEmptyOrder, related_name='expanses', null=True, on_delete=models.SET_NULL)
    wagon = models.ForeignKey(Wagon, related_name='empty_expanses', null=True, on_delete=models.SET_NULL)
