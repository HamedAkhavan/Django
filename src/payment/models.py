from django.db import models
from tickets.models import Ticket

from django.contrib.auth.models import User


# Create your models here.
class Transaction(models.Model):

    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=200)