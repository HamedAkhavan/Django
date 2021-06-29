from django.db import models
from django.contrib.auth.models import User


class TicketType(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Event(models.Model):

    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    address = models.TextField(blank=True)

    @property
    def available_ticket(self):
        tickets = [{
            'id': ticket.ticket_type.id,
            'name': ticket.ticket_type.name,
            'remaining': ticket.quantity - Ticket.objects.filter(event_id=self.id, ticket_type=ticket.ticket_type).count()       
        }for ticket in self.ticket_types.all()]
        return tickets


    def __str__(self):
        return self.name + '_' + str(self.date.date())


class TicketQuantity(models.Model):

    quantity = models.IntegerField()
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, related_name='ticket_types', on_delete=models.CASCADE)
    price = models.FloatField(default=0)

    @property
    def remaining(self):
        return self.quantity - Ticket.objects.filter(event_id=self.event_id, ticket_type=self.ticket_type).count()

    def __str__(self):
        return self.event_id.name + '_' + self.ticket_type.name + '_' + str(self.quantity)

    class Meta:
        verbose_name_plural = 'quantities'

class Ticket(models.Model):
    TICKET_STATUS = [
        ('reserved', 'Reserved'),
        ('paid', 'Paid')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, related_name='tickets', on_delete=models.CASCADE)
    status = models.CharField(max_length=200, default='reserved', choices=TICKET_STATUS)
    ticket_type = models.ForeignKey(TicketType, default=1, on_delete=models.SET_DEFAULT)

    @property
    def price(self):
        for ticket_type in self.event_id.ticket_types.all():
            if ticket_type.ticket_type.id == self.ticket_type.id:
                price = ticket_type.price
                return price

    def __str__(self):
        return self.user.username + '_' + self.event_id.name
