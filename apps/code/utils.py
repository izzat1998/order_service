import datetime

import requests
from docxtpl import DocxTemplate

from apps.core.models import Station, Product
from apps.counterparty.models import Counterparty


class DocxService:
    template = 'apps/utils/application_template.docx'

    @classmethod
    def create_doc_file(cls, application_data):
        territories = ''
        for i in range(len(application_data.get('territories'))):
            if i + 1 != len(application_data.get('territories')):
                territories += application_data.get('territories')[i]['name'] + ', '
            else:
                territories += application_data.get('territories')[i]['name']
        forwarder = Counterparty.objects.filter(id=application_data.get('forwarder_id')).first()
        departure = Station.objects.filter(id=application_data.get('departure_id')).first()
        destination = Station.objects.filter(id=application_data.get('destination_id')).first()
        product = Product.objects.filter(id=application_data.get('product_id')).first()
        fields = {
            'order_number': str(application_data.get('prefix') + application_data.get('number')),
            'date': datetime.datetime.strptime(str(application_data.get('date')), '%Y-%m-%d').strftime('%d.%m.%y'),
            'forwarder': forwarder.name,
            'shipper': application_data.get('shipper'),
            'consignee': application_data.get('consignee'),
            'dep_code': departure.code,
            'departure': departure.name,
            'des_code': destination.code,
            'destination': destination.name,
            'cargo_name': product.name,
            'hc_code': product.hc_code,
            'etcng': product.etcng_code,
            'type': application_data.get('loading_type'),
            'quantity': application_data.get('quantity'),
            'period': application_data.get('period'),
            'conditions_of_carriage': application_data.get('conditions_of_carriage'),
            'agreed_rate': application_data.get('agreed_rate'),
            'border_crossing': application_data.get('border_crossing'),
            'territory': territories,
            'dep_country': application_data.get('departure_country'),
            'des_country': application_data.get('destination_country'),
            'rolling_stock_1': application_data.get('rolling_stock_1'),
            'rolling_stock_2': application_data.get('rolling_stock_2'),
            'paid_telegram': application_data.get('paid_telegram'),
            'container_or_wagon_numbers': application_data.get('containers_or_wagons'),
            'sending_type': application_data.get('sending_type')
        }
        if application_data.get('weight') == "":
            fields['weight'] = application_data.get('container_type')
        else:
            fields['weight'] = application_data.get('weight')
        doc = DocxTemplate(cls.template)
        doc.render(fields)
        doc.save('media/applications/generated_doc.docx')
        application_name = f'{forwarder.name}_{fields["order_number"]}_Заявка на коды по {territories}.pdf'
        return 'home/izzat/order_service/media/applications/generated_doc.docx', application_name


class ConvertToPdf:
    url = 'https://converter.interrail.uz/docx-to-pdf/'

    @classmethod
    def convert(cls, docx_file, file_name):
        with open(docx_file, 'rb') as f:
            docx_data = f.read()
        response = requests.post(cls.url, files={'document': docx_data})
        with open(f'media/applications/{file_name}', 'wb') as f:
            f.write(response.content)
        return 'applications/' + file_name
