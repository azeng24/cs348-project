from django.contrib import admin
from .models import Customer, Shoe, Inventory, Sale

# Register your models here.
admin.site.register(Customer)
admin.site.register(Shoe)
admin.site.register(Inventory)
admin.site.register(Sale)