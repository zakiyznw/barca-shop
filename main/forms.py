# main/forms.py
from django import forms
from main.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # field yang akan muncul di form
        fields = ['name', 'price', 'stock', 'description', 'thumbnail', 'category']

