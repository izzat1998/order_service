from django.db import models

from apps.container_order.models import CounterPartyOrder
from apps.core.models import Wagon, TimeStampedModel
from apps.order.models import WagonOrder


class WagonPreliminaryCost(TimeStampedModel):
    order = models.ForeignKey(WagonOrder, on_delete=models.CASCADE,
                              related_name='wagon_preliminary_costs')
    counterparty = models.ForeignKey(CounterPartyOrder, on_delete=models.CASCADE,
                                     )
    preliminary_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


# Create your models here.
class WagonActualCost(TimeStampedModel):
    counterparty = models.ForeignKey(CounterPartyOrder, on_delete=models.CASCADE)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    wagon_expanse = models.ForeignKey('WagonExpanse', related_name='actual_costs', on_delete=models.CASCADE,
                                      null=True)

    class Meta:
        unique_together = ('counterparty', 'wagon_expanse')


class WagonExpanse(models.Model):

    actual_weight = models.IntegerField(default=60)
    order = models.ForeignKey(WagonOrder, related_name='expanses', null=True, on_delete=models.SET_NULL)
    wagon = models.ForeignKey(Wagon, related_name='expanses', null=True, on_delete=models.SET_NULL)
