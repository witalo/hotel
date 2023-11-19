from django.db import models
from django.forms import model_to_dict


# Create your models here.


class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.CharField(max_length=15, blank=False, null=False, unique=True, default='')
    names = models.CharField(max_length=300, blank=False, null=False)
    phone = models.CharField(max_length=9, blank=True, null=True, default='')
    address = models.CharField(max_length=200, blank=True, null=True, default='')
    is_state = models.BooleanField(default=True)

    def to_json(self):
        dic = model_to_dict(self)
        return dic

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']

    def __str__(self):
        return self.names
