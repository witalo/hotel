import decimal
import os

from django.db import models
# Create your models here.
from django.forms import model_to_dict

from hotel import settings


def get_file_path_product(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.id, ext)
    return os.path.join('photo/', filename)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, blank=False, null=False, unique=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=100, blank=True, null=True, default='')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    product_brand = models.ForeignKey('products.ProductBrand', on_delete=models.CASCADE, default=None)
    price = models.DecimalField('Precio', max_digits=10, decimal_places=2, default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_priority = models.BooleanField('Prioridad', default=False)
    is_state = models.BooleanField('Estado', default=True)

    def get_store(self, u):
        store_set = ProductStore.objects.filter(product=self, subsidiary__user=u)
        if store_set.exists():
            store_obj = store_set.first()
            return model_to_dict(store_obj)
        else:
            store = {'id': 0, 'product': self.name, 'subsidiary': 0, 'quantity': 0}
            return store

    def to_json(self):
        dic = model_to_dict(self)
        return dic

    def get_url(self):
        dic = settings.MEDIA_URL + settings.MEDIA_ROOT
        return dic

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

    def __str__(self):
        return self.name


class ProductBrand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['id']

    def __str__(self):
        return self.name


class ProductStore(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, null=False, blank=False)
    subsidiary = models.ForeignKey('subsidiaries.Subsidiary', on_delete=models.CASCADE, default=None)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    quantity = models.DecimalField('Cantidad', max_digits=10, decimal_places=2, default=0)

    def to_json(self):
        dic = model_to_dict(self)
        return dic

    class Meta:
        verbose_name = 'Almacen'
        verbose_name_plural = 'Almacenes'
        ordering = ['id']
        unique_together = ('product', 'subsidiary')  # product y subsidiary unicos si los dos estan

    def __str__(self):
        name = "{} - {}".format(self.product.name, self.quantity)
        return str(name)
