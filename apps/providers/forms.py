from django import forms

from apps.providers.models import Provider


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['document', 'names', 'phone', 'address']
        labels = {
            'document': 'Documento',
            'names': 'Nombres',
            'phone': 'Celular',
            'address': 'Direccion'
        }
        widgets = {
            'document': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Documento',
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
                    'name': 'names',
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
