from django import forms
from .models import Product, Brand

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields= ['title', 'price', 'description', 'image', 'brand']
        
        widgets = {
            'title' : forms.TextInput(attrs={"class": "form-control","placeholder": "Nhập tên sản phẩm", "pattern": ".{8,}"}),
            'price' : forms.NumberInput(attrs={"min": 10000, "class": "form-control"}),
            'description' : forms.Textarea(attrs={"class": "form-control", "rows": "3"}),
            'brand' : forms.Select(attrs={"class": "form-control"}),
            'image' : forms.FileInput(attrs={"id": "imgInp", "name": "imgInp"})
        }
    
