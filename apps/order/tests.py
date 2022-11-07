from django.test import TestCase

from apps.order.models import Order


class TestOrderModel(TestCase):

    def test_order_create(self):
        order_data = {
            "order_number": 200,
            "lot_number": "1111",
            "date": "2022-10-14",
            "position": "Block train",
            "type": "import",
            "shipment_status": "delivered",
            "payment_status": "issued",
            "shipper": "LLC \"Gallaorol kaliy fosfat\"",
            "consignee": "FE MEDEX",
            "departure_id": 12858,
            "destination_id": 12859,
            "border_crossing": "Келес эксп - Сарыагач эксп",
            "conditions_of_carriage": "FOB-FOR",
            "rolling_stock": "СПС контейнер",
            "departure_country": "Uzbekistan",
            "destination_country": "China",
            "comment": "Hello world",
            "manager": 1,
            "customer": 1}
        order = Order.objects.create(**order_data)
        self.assertEquals(200, order.order_number)
