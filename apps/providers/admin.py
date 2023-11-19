from django.contrib import admin

# Register your models here.
from apps.providers.models import Provider

admin.site.register(Provider)