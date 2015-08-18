from django import forms
from django.utils import timezone

from inventory.models import Item, ItemRequisition


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('location', 'category', 'name', 'material_number',
            'serial_number', 'date_received', 'kit', 'notes', 'sort_by_name',
            'shipment', 'manual')


class CheckInForm(forms.ModelForm):
    """Form to CheckIn a single piece of equipment. Designed to be used
    in a FormSet"""
    selected = forms.BooleanField()

    class Meta:
        model = ItemRequisition
        fields = ('checked_in_on',)

    def clean(self):
        if self.cleaned_data.get('selected'):
            self.cleaned_data['checked_in_on'] = timezone.now()


class CheckOutForm(forms.ModelForm):
    """Form to create a new ItemRequistion. Designed to be used in a FormSet."""
    selected = forms.BooleanField()

    class Meta:
        model = ItemRequisition
        fields = ('item', 'checked_out_by',)

    def save(self):
        if self.cleaned_data.get('selected'):
            super(CheckoutForm, self).save()
