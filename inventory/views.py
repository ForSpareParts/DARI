from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from extra_views import ModelFormSetView

from inventory import models, forms


class HomepageView(TemplateView):
    template_name = 'index.html'


class CheckOutView(ModelFormSetView):
    template_name = 'checkout.html'
    model = models.ItemRequisition
    form_class = forms.CheckOutForm
    extra = 0

    # TODO: We need to prepopulate all forms with available items. However,
    # get_initial only populates extra forms. The number of extra forms
    # (self.extra) is a static value. We need to make extra dynamic or find a
    # different way of using this view
    def get_initial(self):
        available_items = models.Item.objects.filter(current_qty__gt=0)
        initial = [{'item':item} for item in available_items]
        return initial

    def get_queryset(self):
        return models.ItemRequisition.objects.none()

    def get_success_url(self):
        return reverse('homepage')


class CheckInView(ModelFormSetView):
    template_name = 'checkin.html'
    model = models.ItemRequisition
    form_class = forms.CheckInForm
    extra = 0

    def get_success_url(self):
        return reverse('homepage')
