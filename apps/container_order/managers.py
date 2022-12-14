from django.db import models


class ContainerOrderManager(models.Manager):
    def get_by_order_number(self, order_number):
        return (
            self.filter(order__order_number=order_number)
            .select_related("order__departure", "order__destination", "product")
            .prefetch_related(
                "container_types__container_preliminary_costs__counterparty__category",
                "container_types__container_preliminary_costs__counterparty__counterparty",
                "container_types__expanses__actual_costs__counterparty__counterparty",
                "container_types__expanses__actual_costs__counterparty__category",
                "container_types__expanses__container",
                "order__counterparties__category",
                "order__counterparties__counterparty",
            )
        )

    def get_list(self):
        return self.filter(order__visible=True).select_related("order__departure", "order__destination",
                                                               "product").order_by(
            "-order__order_number")
