from django.test import TestCase
from django.utils import timezone

from inventory import models

# Create your tests here.

class ModelTestCase(TestCase):
    '''Tests models'''

    def test_item(self):
        item1 = models.Item(
            location='SYKES',
            category='Category 1',
            name='Item 1',
            serial_number='123456',
            date_received=timezone.now())
        item1.save()
        self.assertEqual(item1.qty_at_inventory, 1)
        self.assertEqual(item1.current_qty, 1)
        item1.qty_at_inventory=0
        item1.save()
        self.assertEqual(item1.qty_at_inventory, 1)
        self.assertEqual(item1.current_qty, 1)
