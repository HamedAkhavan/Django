from django.contrib import admin
from payment.models import Transaction
# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Transaction, TransactionAdmin)