import logging
from datetime import datetime
from django.core.management.base import BaseCommand
from inflection import underscore
from pytz import timezone
from xlrd import (open_workbook, xldate_as_tuple,
    XL_CELL_EMPTY, XL_CELL_TEXT, XL_CELL_NUMBER, XL_CELL_DATE,
    XL_CELL_BOOLEAN, XL_CELL_ERROR, XL_CELL_BLANK)

from inventory.forms import ItemForm
from inventory.models import Item

logger = logging.getLogger(__name__)

TZ = timezone('US/Eastern')

DEFAULT_COLUMNS = (
    'location', 'category', 'name', 'material_number', 'serial_number',
    'date_received', 'kit', 'notes', 'sort_by_name', 'shipment', 'manual')

COLUMN_MAP = {
    'item': 'name', 'material#': 'material_number', '': 'manual'}

LABEL_TRIGGER = 'Location'
DATA_TRIGGER = 'SYKES'

class Command(BaseCommand):
    help = "Loads an inventory file"

    def add_arguments(self, parser):
        parser.add_argument('inventory_file', nargs=1,
            help='excel file containing the inventory')
        parser.add_argument('sheet_name', nargs=1,
            help='excel sheet name to load')

    def handle(self, *args, **options):
        workbook = open_workbook(options['inventory_file'][0])
        sheet = workbook.sheet_by_name(options['sheet_name'][0])

        columns = DEFAULT_COLUMNS
        for row_index in xrange(len(sheet.col(0))):
            row = sheet.row(row_index)
            if row[0].value == LABEL_TRIGGER:
                columns = []
                for cell in row:
                    label = '_'.join(cell.value.lower().split())
                    label = underscore(label)
                    columns.append(
                        COLUMN_MAP[label] if label in COLUMN_MAP else label)
            elif row[0].value == DATA_TRIGGER:
                item_data = {}
                for index, cell in enumerate(row):
                    if cell.ctype == XL_CELL_DATE:
                        value = xldate_as_tuple(cell.value, workbook.datemode)
                        value = TZ.localize(datetime(*value))
                    elif cell.ctype in (
                            XL_CELL_TEXT, XL_CELL_NUMBER, XL_CELL_BOOLEAN):
                        value = cell.value
                    else:
                        value = None
                    item_data[columns[index]] = value
                form = ItemForm(item_data)
                if form.is_valid():
                    item = form.instance
                    matching_items = Item.objects.filter(
                        category=item.category,
                        name=item.name,
                        material_number=item.material_number,
                        serial_number=item.serial_number,
                        superceded_by=None)
                    if item.notes.lower().startswith('qty'):
                        numbers = nums.findall(item.notes.lower())
                        if number:
                            item.qty_at_inventory = numbers[0]
                        else:
                            item.qty_at_inventory = 1
                    else:
                        item.qty_at_inventory = 1
                    form.save()
                    if matching_items:
                        matching_items.update(superceded_by=form.instance)
                else:
                    print('Error row {0}'.format(row_index + 1))
                    for key, error in form.errors.items():
                        print(' ==> {0}: {1}'.format(key, repr(error)))
