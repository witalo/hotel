from django import forms

from apps.accounts.models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'type', 'initial', 'subsidiary']
        labels = {
            'name': 'Descripcion',
            'type': 'Tipo',
            'initial': 'Monto Inicial',
            'subsidiary': 'Sede'
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre caja/cuenta',
                    'id': 'name',
                    'name': 'name',
                    'required': 'required'
                }
            ),
            'type': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Tipo',
                    'id': 'type',
                    'name': 'type'
                }
            ),
            'initial': forms.NumberInput(
                attrs={
                    'class': 'form-control text-right',
                    'placeholder': '0.00',
                    'id': 'initial',
                    'name': 'initial'
                }
            ),
            'subsidiary': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Sede',
                    'id': 'subsidiary',
                    'name': 'subsidiary'
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        new_name = name.upper()
        return new_name
