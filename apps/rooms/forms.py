from django import forms

from apps.rooms.models import RoomGroup, Room, RoomType, RoomState


class RoomGroupForm(forms.ModelForm):
    class Meta:
        model = RoomGroup
        fields = ['name']
        labels = {
            'name': 'Descripcion'
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripcion',
                    'id': 'name',
                    'name': 'name'
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        new_name = name.upper()
        return new_name


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'name', 'capacity', 'group', 'type', 'state', 'noon', 'day', 'refund', 'person', 'is_state']
        labels = {
            'number': 'Numero Habitacion',
            'name': 'Nombre Habitacion',
            'capacity': 'Capacidad Habitacion',
            'group': 'Grupo Habitacion',
            'type': 'Clase Habitacion',
            'state': 'Estados Habitacion',
            'noon': 'Precio 12 horas',
            'day': 'Precio 24 horas',
            'refund': 'Precio Reintegro',
            'person': 'Precio por persona adicional',
            'is_state': 'Activo',
        }
        widgets = {
            'number': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0',
                    'step': 1,
                    'min': 0,
                    'id': 'number',
                    'name': 'number',
                    'required': 'required'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre Habitacion',
                    'maxlength': 200,
                    'id': 'name',
                    'name': 'name',
                    'required': 'required'
                }
            ),
            'capacity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0',
                    'step': 1,
                    'min': 0,
                    'id': 'capacity',
                    'name': 'capacity',
                    'required': 'required'
                }
            ),
            'group': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Grupo',
                    'id': 'group',
                    'name': 'group',
                    'required': 'required'
                }
            ),
            'type': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Tipo',
                    'id': 'type',
                    'name': 'type',
                    'required': 'required'
                }
            ),
            'state': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Estado',
                    'id': 'state',
                    'name': 'state',
                    'required': 'required'
                }
            ),
            'noon': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0.00',
                    'step': '0.01',
                    'min': 0,
                    'id': 'noon',
                    'name': 'noon',
                    'required': 'required'
                }
            ),
            'day': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0.00',
                    'step': '0.01',
                    'min': 0,
                    'id': 'day',
                    'name': 'day',
                    'required': 'required'
                }
            ),
            'refund': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0.00',
                    'step': '0.01',
                    'min': 0,
                    'id': 'refund',
                    'name': 'refund',
                    'required': 'required'
                }
            ),
            'person': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0.00',
                    'step': '0.01',
                    'min': 0,
                    'id': 'person',
                    'name': 'person',
                    'required': 'required'
                }
            ),
            'is_state': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input ml-2',
                    'id': 'is_state',
                    'name': 'is_state'
                }
            )
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        new_name = name.upper()
        return new_name


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['name']
        labels = {
            'name': 'Tipo de Habitacion'
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripcion tipo',
                    'id': 'name',
                    'name': 'name'
                }
            )
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        new_name = name.upper()
        return new_name


class RoomStateForm(forms.ModelForm):
    class Meta:
        model = RoomState
        fields = ['name', 'color', 'type']
        labels = {
            'name': 'Estado de Habitacion',
            'color': 'Color Habitacion',
            'type': 'Tipo de estado'
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripcion estado',
                    'id': 'name',
                    'name': 'name'
                }
            ),
            'type': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Tipo',
                    'id': 'type',
                    'name': 'type',
                    'required': 'required'
                }
            ),
            'color': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripcion estado',
                    'data-original-title': "",
                    'title': "",
                    'id': 'color',
                    'name': 'color'
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        new_name = name.upper()
        return new_name

    def clean_color(self):
        color = self.cleaned_data['color']
        new_color = color.replace("#", "")
        return new_color
