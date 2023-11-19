import decimal

from django.db import models
from apps.users.models import User


# Create your models here.


class Account(models.Model):
    TYPE_CHOICES = (('E', 'CAJA DE EFECTIVO'), ('B', 'CUENTA BANCARIA'))
    id = models.AutoField(primary_key=True)
    name = models.CharField('Nombre', max_length=50)
    type = models.CharField('Tipo', max_length=1, choices=TYPE_CHOICES)
    initial = models.DecimalField(max_digits=10, decimal_places=2, default='0')
    subsidiary = models.ForeignKey('subsidiaries.Subsidiary', on_delete=models.SET_NULL, null=True, blank=True)
    create_at = models.DateTimeField(auto_now=True)
    is_state = models.BooleanField(default=True)

    def get_status(self):
        status = 'C'
        payment_set = Payments.objects.filter(account=self, status='R', type__in=['A', 'C'])
        if payment_set.exists():
            status = payment_set.last().type
            return status
        else:
            return status

    def total(self):
        from apps.accounts.views import get_total
        total = get_total(account_obj=self)
        t = decimal.Decimal(0.00)
        if total:
            t = total[0].get('total')
        return t

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'
        ordering = ['id']

    def __str__(self):
        return self.name


class Payments(models.Model):
    TYPE_CHOICES = (('I', 'Ingreso'), ('E', 'Egreso'), ('A', 'Apertura'), ('C', 'Cierre'))
    STATUS_CHOICES = (('R', 'Realizado'), ('A', 'Anulado'))
    PAYMENT_CHOICES = (('P', 'Pagado'), ('C', 'Credito'))
    id = models.AutoField(primary_key=True)
    status = models.CharField('Estado', max_length=1, choices=STATUS_CHOICES, default='R')
    type = models.CharField('Tipo', max_length=1, choices=TYPE_CHOICES)
    payment = models.CharField('Pago', max_length=1, choices=PAYMENT_CHOICES, default='P')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField('Codigo de operacion', max_length=50, null=True, blank=True)
    description = models.CharField('Descripcion de la operacion', max_length=250, default='-')
    amount = models.DecimalField('Monto', max_digits=10, decimal_places=2, default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    date_payment = models.DateField(null=True, blank=True)
    user = models.ForeignKey('users.User', verbose_name='Usuario', on_delete=models.CASCADE, null=True, blank=True)
    account = models.ForeignKey('accounts.Account', verbose_name='E/B', on_delete=models.SET_NULL, null=True, blank=True)
    number = models.IntegerField(verbose_name='Numero', null=True, blank=True)
    subsidiary = models.ForeignKey('subsidiaries.Subsidiary', verbose_name='Filial', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['id']

    def __str__(self):
        return str(self.id)