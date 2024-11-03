from django.urls import path
from .views import SaleList, CreateSale, UpdateSale, DeleteSale, InventoryList

urlpatterns = [
    path('', InventoryList.as_view(), name="inventory_list"),
    path('sales/', SaleList.as_view(), name='sale_list'),
    path('sales/add/', CreateSale.as_view(), name='sale_add'),
    path('sales/edit/<int:pk>/', UpdateSale.as_view(), name='sale_edit'),
    path('sales/delete/<int:pk>/', DeleteSale.as_view(), name='sale_delete'),
]