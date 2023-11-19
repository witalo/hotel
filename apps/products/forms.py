from django import forms

from apps.products.models import ProductBrand, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'description', 'product_brand', 'price', 'is_priority']
        labels = {
            'code': 'Codigo producto',
            'name': 'Nombre producto',
            'description': 'Descripcion producto',
            'product_brand': 'Marca producto',
            'price': 'Precio producto',
            'is_priority': 'Prioridad producto',
        }
        widgets = {
            'code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su codigo',
                    'id': 'code',
                    'name': 'code',
                    'maxlength': 100,
                    'required': 'required'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese nombre producto',
                    'maxlength': 200,
                    'id': 'name',
                    'name': 'name',
                    'required': 'required'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese descripcion producto',
                    'maxlength': 200,
                    'rows': 3,
                    'id': 'description',
                    'name': 'description'
                }
            ),
            'product_brand': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'product_brand',
                    'name': 'product_brand',
                    'required': 'required'
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control text-right',
                    'placeholder': '0.00',
                    'min': 0.00,
                    'step': 0.01,
                    'id': 'price',
                    'name': 'price',
                    'required': 'required'
                }
            ),
            'is_priority': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input ml-2 mt-2',
                    'id': 'is_priority',
                    'name': 'is_priority',
                    'required': 'required'
                }
            )
        }

    def clean_code(self):
        code = self.cleaned_data['code']
        new_code = code.upper()
        return new_code

    def clean_name(self):
        name = self.cleaned_data['name']
        new_name = name.upper()
        return new_name


class ProductBrandForm(forms.ModelForm):
    class Meta:
        model = ProductBrand
        fields = ['name']
        labels = {
            'name': 'Nombre de la marca'
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre Marca',
                    'id': 'name',
                    'name': 'name',
                    'required': 'required'
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        n_name = name.upper()
        return n_name