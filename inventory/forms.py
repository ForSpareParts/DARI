from django.forms import ModelForm
from inventory.models import Item


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('location', 'category', 'name', 'material_number',
            'serial_number', 'date_received', 'kit', 'notes', 'sort_by_name',
            'shipment', 'manual')
