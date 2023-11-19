import decimal

from django.db import models
from django.forms import model_to_dict


# Create your models here.
from apps.orders.models import Order


class RoomGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    is_state = models.BooleanField(default=True)

    def to_json(self):
        dic = model_to_dict(self)
        return dic

    class Meta:
        verbose_name = 'Grupo Habitacion'
        verbose_name_plural = 'Grupos Habitaciones'
        ordering = ['id']

    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(verbose_name='Numero Habitacion', null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    capacity = models.IntegerField(verbose_name='AFORO DE PERSONAS', null=True, blank=True, default='')
    group = models.ForeignKey('rooms.RoomGroup', on_delete=models.CASCADE, null=True, blank=True)
    type = models.ForeignKey('rooms.RoomType', on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey('rooms.RoomState', on_delete=models.CASCADE, null=True, blank=True, default=None)
    noon = models.DecimalField('Precio 12 Hora', max_digits=10, decimal_places=2, default=0)
    day = models.DecimalField('Precio 24 Hora', max_digits=10, decimal_places=2, default=0)
    refund = models.DecimalField('Precio Reintegro', max_digits=10, decimal_places=2, default=0)
    person = models.DecimalField('Precio adicional por persona', max_digits=10, decimal_places=2, default=0)
    is_state = models.BooleanField(default=True)

    def get_order(self):
        if self.state.type == 'R' or self.state.type == 'O' or self.state.type == 'X':
            order_set = Order.objects.filter(room=self, status='P')
            if order_set.exists():
                order_obj = order_set.last()
                return order_obj
            else:
                return None

    class Meta:
        verbose_name = 'Habitacion'
        verbose_name_plural = 'Habitaciones'
        ordering = ['id']

    def __str__(self):
        return str(self.id)


class RoomType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    is_state = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Tipo Habitacion'
        verbose_name_plural = 'Tipo Habitaciones'
        ordering = ['id']

    def __str__(self):
        return self.name


class RoomState(models.Model):
    TYPE_CHOICES = (
        ('D', 'DISPONIBLE'),
        ('R', 'RESERVADO'),
        ('O', 'OCUPADO'),
        ('M', 'MANTENIMIENTO'),
        ('X', 'REINTEGRO')
    )
    id = models.AutoField(primary_key=True)
    type = models.CharField('TIPO', max_length=1, choices=TYPE_CHOICES, default='D')
    name = models.CharField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=200, default='08AB05')
    is_state = models.BooleanField(default=True)

    def get_color(self):
        color = "{}{}".format('#', self.color)
        return color

    class Meta:
        verbose_name = 'Estado Habitacion'
        verbose_name_plural = 'Estados Habitaciones'
        ordering = ['id']

    def __str__(self):
        return self.name
