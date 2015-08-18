from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.

class InventoryUser(AbstractUser):
    '''Custom user model in case we need to extend the user model later'''
    USERNAME_FIELD = 'username'

class Item(models.Model):
    '''Describes a single type of inventoried item.'''

    location = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    material_number = models.CharField(max_length=255, blank=True, default='')
    serial_number = models.CharField(max_length=255, blank=True, default='')
    date_received = models.DateField(blank=True, null=True)
    kit = models.CharField(max_length=255, blank=True, default='')
    notes = models.TextField(blank=True, default='')
    sort_by_name = models.CharField(max_length=255, blank=True, default='')
    shipment = models.CharField(max_length=255, blank=True, default='')
    manual = models.TextField(blank=True, default='')
    qty_at_inventory = models.PositiveIntegerField(blank=True, default=1)
    inventory_loaded_on = models.DateTimeField(auto_now_add=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    current_qty = models.IntegerField(blank=True)
    superceded_by = models.ForeignKey('Item', blank=True, null=True)

    class Meta:
        unique_together = (
            ('category', 'name', 'material_number', 'serial_number',
                'superceded_by'),)

    def get_qty_as_of(self, as_of):
        items = (Item.objects
            .filter(inventory_loaded_on__lte=as_of))
        if items:
            item = items.latest('inventory_loaded_on')
        out_cnt = (ItemRequisition.objects
            .filter(item=item, checked_out_on__lte=as_of, check_in_on=None))
        return item.qty_at_inventory - Item

    def save(self, *args, **kwargs):
        # set the current qty
        assert not self.serial_number or self.qty_at_inventory in (0, 1), \
            _('qty must be 0 or 1 for items with a serial number')
        if getattr(self, 'pk', None):
            self.current_qty = self.get_qty_as_of(timezone.now())
        else:
            self.current_qty = self.qty_at_inventory
        super(Item, self).save(*args, **kwargs)
        # supercede any existing item of same name
        (Item.objects
            .filter(
                superceded_by=None,
                name=self.name,
                category=self.category,
                material_number=self.material_number,
                serial_number=self.serial_number)
            .update(superceded_by=self))
        # move any open reqs on superceded item to self
        (ItemRequisition.objects
            .filter(
                checked_in_on=None,
                item__name=self.name,
                item__serial_number=self.serial_number,
                item__category=self.category)
            .update(item=self))
        


class ItemRequisition(models.Model):
    '''Represents an Agent's checkout of an item'''

    item = models.ForeignKey('Item')
    checked_out_by = models.CharField(max_length=255)
    checked_out_on = models.DateTimeField(auto_now_add=True)
    checked_in_on = models.DateTimeField(blank=True, null=True)
    last_modified_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        assert self.item.current_qty > 0, \
            'There are no {0} to check out'.format(item.name)
        super(ItemRequisition, self).save(*args, **kwargs)
        self.item.save()
