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
    material_number = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, blank=True, default='')
    date_received = models.DateField()
    kit = models.CharField(max_length=255, blank=True, default='')
    notes = models.TextField(blank=True, default='')
    sort_by_name = models.CharField(max_length=255)
    manual = models.TextField(blank=True, default='')
    qty_at_inventory = models.PositiveIntegerField(blank=True, default=1)
    inventory_loaded_on = models.DateTimeField(auto_now_add=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    current_qty = models.IntegerField(blank=True)
    superceded_by = models.ForeignKey('Item', blank=True, null=True)

    class Meta:
        unique_together = (
            ('category', 'name', 'serial_number', 'superceded_by'),)

    def get_qty_as_of(self, as_of):
        item = (Item.objects
            .filter(inventory_loaded_on__lte=as_of)
            .latest('inventory_loaded_on'))
        out_cnt = (ItemRequisition.objects
            .count(item=item, checked_out_on__lte=as_of, check_in_on=None))
        return item.qty_at_inventory - Item

    def save(self, *args, **kwargs):
        # set the current qty
        assert not serial_number or qty_at_inventory in (0, 1), _('qty must '
            'be 0 or 1 for items with a serial number')
        if getattr(self, 'pk', None):
            self.current_qty = self.qty_at_inventory
        else:
            self.current_qty = self.get_qty_as_of(timezone.now())
        # supercede any existing item of same name
        (Item.objects
            .filter(superceded_by=None, name=self.name, category=self.category)
            .update(superceded_by=self))
        # move any open reqs on superceded item to self
        (ItemRequisition.objects
            .filter(
                checked_in_on=None,
                item__name=self.name,
                item__serial_number=self.serial_number,
                item__category=self.category)
            .update(item=self))
        super(Item, self).save(*args, **kwargs)
        


class ItemRequisition(models.Model):
    '''Represents an Agent's checkout of an item'''

    item = models.ForeignKey('Item')
    checked_out_on = models.DateTimeField(auto_now_add=True)
    checked_in_on = models.DateTimeField()
    agent_identifier = models.CharField(max_length=255)
    last_modified_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        assert item.current_qty > 0, 'There are none of this item to check out'
        super(ItemRequisition, self).save(*args, **kwargs)
        self.item.save()
