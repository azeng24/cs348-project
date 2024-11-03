from django import forms
from .models import Sale

class SaleForm(forms.ModelForm):
    sale_date = forms.DateField(
        label="Sale date",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    class Meta:
        model = Sale
        fields = ['inventory', 'customer', 'sale_date', 'sale_price', 'quantity']