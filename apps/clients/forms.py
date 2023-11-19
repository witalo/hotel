from django import forms

from apps.clients.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['document', 'names', 'phone', 'address']
        labels = {
            'document': 'Numero Documento',
            'names': 'Nombres & Apellidos',
            'phone': 'Celular',
            'address': 'Direccion'
        }
        widgets = {
            'document': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Numero documento',
                    'id': 'document',
                    'name': 'document',
                    'required': 'required'
                }
            ),
            'names': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombres y Apellidos',
                    'id': 'names',
                    'name': 'names'
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
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Direccion',
                    'id': 'address',
                    'name': 'address'
                }
            )
        }

    def clean_names(self):
        names = self.cleaned_data['names']
        new_names = names.upper()
        return new_names
