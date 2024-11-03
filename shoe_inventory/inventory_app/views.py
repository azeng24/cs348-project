from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import Sale, Inventory
from .forms import SaleForm

# Create your views here.
class SaleList(ListView):
    model = Sale
    template_name = 'sales/sale_list.html'

class CreateSale(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sale_list')

class UpdateSale(UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sale_list')

class DeleteSale(DeleteView):
    model = Sale
    template_name = 'sales/confirm_delete.html'
    success_url = reverse_lazy('sale_list')

class InventoryList(ListView):
    model = Inventory
    template_name = 'inventory/inventory_list.html'