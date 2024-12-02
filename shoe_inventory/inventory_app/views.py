from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.db import connection
from .models import Sale, Inventory, Customer
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

def report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    selected_customers = request.GET.getlist('customer')
    selected_sizes = request.GET.getlist('size')

    sales = []
    report = []

    if (start_date and end_date) or selected_customers or selected_sizes:
        params = []
        sale_query = """
            SELECT 
                s.id,
                (sh.brand || ' ' || sh.model || ' ' || sh.name) AS shoe_name, 
                i.size, 
                c.name, 
                s.sale_date, 
                s.sale_price, 
                s.quantity
            FROM inventory_app_sale s
            JOIN inventory_app_inventory i ON i.id = s.inventory_id
            JOIN inventory_app_shoe sh ON sh.sku = i.shoe_id
            JOIN inventory_app_customer c ON c.id = s.customer_id
            WHERE 1=1
        """

        summary_query = """
            SELECT
                SUM(s.quantity) AS total_sales_quantity,
                SUM(s.sale_price * s.quantity) AS total_sales,
                SUM((s.sale_price - i.buy_price) * s.quantity) AS total_profit,
                SUM(s.sale_price * s.quantity)*1.0/SUM(s.quantity) AS avg_sale_price,
                SUM((s.sale_price - i.buy_price) * s.quantity)*1.0/(SUM(i.buy_price * s.quantity))*100 AS roi
            FROM inventory_app_sale s
            JOIN inventory_app_inventory i ON i.id = s.inventory_id
            JOIN inventory_app_customer c ON c.id = s.customer_id
            WHERE 1=1
        """

        if start_date and end_date:
            sale_query += " AND s.sale_date BETWEEN %s AND %s"
            summary_query += " AND s.sale_date BETWEEN %s AND %s"
            params.extend([start_date, end_date])

        if selected_customers:
            sale_query += " AND c.id IN (" + ", ".join(["%s"] * len(selected_customers)) + ")"
            summary_query += " AND c.id IN (" + ", ".join(["%s"] * len(selected_customers)) + ")"
            params.extend(selected_customers)

        if selected_sizes:
            sale_query += " AND i.size IN (" + ", ".join(["%s"] * len(selected_sizes)) + ")"
            summary_query += " AND i.size IN (" + ", ".join(["%s"] * len(selected_sizes)) + ")"
            params.extend(selected_sizes)

        with connection.cursor() as cursor:
            cursor.execute(sale_query, params)
            sales = cursor.fetchall()
            cursor.execute(summary_query, params)
            report = cursor.fetchone()

    customers = Customer.objects.all().order_by('name')
    sizes = Inventory.objects.values_list('size', flat=True).distinct().order_by('size')

    return render(
        request, 
        'sales/generate_report.html',
        {
            'customers': customers,
            'sizes': sizes,
            'sales': sales,
            'report': report,
        })