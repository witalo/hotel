import os
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.id, ext)
    return os.path.join('avatar/', filename)


class User(AbstractUser):
    document = models.CharField('Numero Documento', max_length=15, null=True, blank=True)
    phone = models.CharField('Celular', max_length=15, null=True, blank=True)
    avatar = models.ImageField('Foto', upload_to=get_file_path, blank=True, null=True)
    subsidiary = models.ForeignKey('subsidiaries.Subsidiary', on_delete=models.CASCADE, null=True, blank=True)

    REQUIRED_FIELDS = ['email', 'document', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['id']

    def __str__(self):
        return self.email

