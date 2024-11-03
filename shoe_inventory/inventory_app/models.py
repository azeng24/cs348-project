from django.db import models

# Create your models here.
from django.db import models
from django.db.models import F
from django.core.exceptions import ValidationError

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.name
    
class Shoe(models.Model):
    sku = models.CharField(max_length=50, primary_key=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    retail_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.brand} {self.model} {self.name}"
    
class Inventory(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    quantity = models.IntegerField()
    buy_date = models.DateField()
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.shoe} Size {self.size}"

class Sale(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    sale_date = models.DateField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.pk: # update sale
            sale = Sale.objects.get(pk = self.pk)
            qty = self.inventory.quantity + sale.quantity - self.quantity
        else: # new sale
            qty = self.inventory.quantity - self.quantity
        
        # check if there is enough inventory
        if qty < 0:
            raise ValidationError("Not enough inventory for sale")
        
        # decrease inventory if valid
        self.inventory.quantity = qty
        self.inventory.save(update_fields=['quantity'])

        # save sale instance
        return super().save(*args, *kwargs)

    def delete(self, *args, **kwargs):
        # adjust inventory
        self.inventory.quantity += self.quantity
        self.inventory.save(update_fields=['quantity'])

        # delete sale instance 
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"Sale {self.id}: {self.inventory}"