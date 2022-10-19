import xlrd

from core.models import Station


def add_stations():
    workbook = xlrd.open_workbook("stations.xlsx")
    worksheet = workbook.sheet_by_index(0)
    for i in range(1, 8475):
        if "(ОП.)" not in worksheet.cell(i, 0).value:
            Station.objects.get_or_create(
                name=worksheet.cell(i, 0).value,
                code=str(worksheet.cell(i, 3).value).replace(".0", ''),
                railway_name=worksheet.cell(i, 2).value
            )
