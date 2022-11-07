from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order'

    # {
    #     "order": {
    #         "order_number": 111,
    #         "lot_number": "1111",
    #         "date": "2022-10-14",
    #         "position": "Block train",
    #         "type": "import",
    #         "shipment_status": "delivered",
    #         "payment_status": "issued",
    #         "shipper": "LLC \"Gallaorol kaliy fosfat\"",
    #         "consignee": "FE MEDEX",
    #         "departure_id": 23,
    #         "destination": 123,
    #         "border_crossing": "Келес эксп - Сарыагач эксп",
    #         "conditions_of_carriage": "FOB-FOR",
    #         "rolling_stock": null,
    #         "departure_country": "Uzbekistan",
    #         "destination_country": "China",
    #         "comment": "Hello world",
    #         "manager": 1,
    #         "customer": 1,
    #         "counterparties": [
    #             {
    #                 "category_id": 11,
    #                 "counterparty_id": 4
    #
    #             }
    #         ]
    #     },
    #     "sending_type": "single",
    #     "product_id": 121,
    #     "container_types": [
    #         {
    #             "agreed_rate": "500.00",
    #             "quantity": 35,
    #             "container_type": "40HC",
    #             "container_preliminary_costs": [
    #                 {
    #                     "category_id": 11,
    #                     "counterparty_id": 4,
    #                     "preliminary_cost": "1500.00"
    #
    #                 }
    #             ],
    #             "expanses": [
    #                 {
    #                     "container": "MSCU7128598",
    #                     "category_id": 11,
    #                     "counterparty_id": 4,
    #                     "actual_cost": "5000.00"
    #                 }
    #             ]
    #         }
    #     ]
    # }