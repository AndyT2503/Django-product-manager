from django import forms
from .models import Product, Brand
from django.contrib.auth.forms import AuthenticationForm
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth import authenticate


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
    

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "username"}) ,max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "password"}), required=True)
    remember_me = forms.BooleanField(required=False,widget= forms.CheckboxInput(attrs={"value": "Remember Me"}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user    

