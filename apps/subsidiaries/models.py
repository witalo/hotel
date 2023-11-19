from django.db import models


class Subsidiary(models.Model):
    id = models.AutoField(primary_key=True)
    serial = models.CharField(max_length=4, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=45, null=True, blank=True)
    email = models.EmailField(max_length=45, null=True, blank=True)
    ruc = models.CharField(max_length=11, null=True, blank=True)
    business = models.CharField('Razón social', max_length=150, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    token = models.CharField(max_length=500, null=True, blank=True)
    is_state = models.BooleanField('Estado', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Filial'
        verbose_name_plural = 'Filiales'
