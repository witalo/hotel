from django.contrib.auth.forms import AuthenticationForm
from django import forms

from apps.users.models import User


class FormLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['id'] = 'username'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['type'] = 'text'
        self.fields['username'].widget.attrs['placeholder'] = 'Usuario'
        self.fields['password'].widget.attrs['id'] = 'password'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password'].widget.attrs['type'] = 'password'


class UserForm(forms.ModelForm):
    password_a = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'id': 'password_a',
            'required': 'required',
        }
    ))
    password_b = forms.CharField(label='Contraseña de confirmacion', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente su contraseña',
            'id': 'password_b',
            'required': 'required',
        }
    ))

    class Meta:
        model = User
        fields = ['username', 'document', 'first_name', 'last_name', 'phone', 'email', 'subsidiary', 'is_active']
        labels = {
            'username': 'Usuario',
            'document': 'Documento',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'phone': 'Celular',
            'email': 'Correo',
            'subsidiary': 'Filial',
            'is_active': 'Activo'
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Usuario',
                    'id': 'username',
                    'name': 'username',
                    'required': 'required'
                }
            ),
            'document': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Documento',
                    'id': 'document',
                    'name': 'document',
                    'required': 'required'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombres',
                    'id': 'first_name',
                    'name': 'first_name',
                    'required': 'required'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Apellidos',
                    'id': 'last_name',
                    'name': 'last_name',
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
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Correo',
                    'id': 'email',
                    'name': 'email',
                    'required': 'required'
                }
            ),
            'subsidiary': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'placeholder': 'Filial',
                    'id': 'subsidiary',
                    'name': 'subsidiary',
                    'required': 'required'
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    'id': 'is_active',
                    'name': 'is_active'
                }
            )
        }

    def clean_password_b(self):
        password_a = self.cleaned_data.get('password_a')
        password_b = self.cleaned_data.get('password_b')
        if password_a != password_b:
            raise forms.ValidationError('Contraseñas no coinciden')
        return password_b

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password_a'])
    #     if commit:
    #         user.save()
    #     return user
