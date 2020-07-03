from django import forms
from .models import Product, Brand
from ckeditor.widgets import CKEditorWidget

class ProductForm(forms.ModelForm):
    #description  = forms.CharField(widget= CKEditorWidget())
    class Meta:
        model = Product
        fields= '__all__'
        
        widgets = {
            'title' : forms.TextInput(attrs={"class": "form-control","placeholder": "Nhập tên sản phẩm", "pattern": ".{8,}"}),
            'price' : forms.NumberInput(attrs={"min": 10000, "class": "form-control"}),
            'description' : forms.Textarea(attrs={"class": "form-control", "rows": "2"}),
            'brand' : forms.Select(attrs={"class": "form-control"}),
            'image' : forms.FileInput(attrs={"id": "imgInp", "name": "imgInp"})
        }
    
