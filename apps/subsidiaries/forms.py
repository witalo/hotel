from django import forms

from apps.subsidiaries.models import Subsidiary


class SubsidiaryForm(forms.ModelForm):
    class Meta:
        model = Subsidiary
        fields = ['serial', 'name', 'phone', 'email', 'address', 'ruc', 'business']
        labels = {
            'serial': 'Serie',
            'name': 'Nombre filial',
            'phone': 'Celular filial',
            'email': 'Correo filial',
            'address': 'Direccion filial',
            'ruc': 'Ruc',
            'business': 'Empresa'
        }
        widgets = {
            'serial': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Numero serie',
                    'id': 'serial',
                    'name': 'serial',
                    'required': 'required'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre filial',
                    'id': 'name',
                    'name': 'name',
                    'required': 'required'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Celular',
                    'id': 'phone',
                    'name': 'phone'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'correo@example.com',
                    'id': 'email',
                    'name': 'email'
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Direccion filial',
                    'id': 'address',
                    'name': 'address'
                }
            ),
            'ruc': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ruc empresa',
                    'id': 'ruc',
                    'name': 'ruc'
                }
            ),
            'business': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre empresa',
                    'id': 'business',
                    'name': 'business'
                }
            )
        }

    def clean_name(self):
        names = self.cleaned_data['name']
        new_names = names.upper()
        return new_names
