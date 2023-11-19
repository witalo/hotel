from django.contrib import admin

# Register your models here.
from apps.accounts.models import Account, Payments

admin.site.register(Account)
admin.site.register(Payments)