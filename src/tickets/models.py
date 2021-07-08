from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):

    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    address = models.TextField(blank=True)

    @property
    def available_ticket(self):
        tickets = [{
            'id': ticket.ticket_type.id,
            'name': ticket.ticket_type.name,
            'remaining': ticket.quantity - Ticket.objects.filter(event=self.id, ticket_type=ticket.ticket_type).count()       
        }for ticket in self.ticket_types.all()]
        return tickets


    def __str__(self):
        return self.name + '_' + str(self.date.date())

class TicketType(models.Model):

    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    event = models.ForeignKey(Event, related_name='ticket_types', default=0, on_delete=models.CASCADE)
    price = models.FloatField(default=0)

    @property
    def remaining(self):
        return self.quantity - Ticket.objects.filter(ticket_type=self).count()

    def __str__(self):
        return self.event.name + '_' + self.name
        
class Ticket(models.Model):
    TICKET_STATUS = [
        ('reserved', 'Reserved'),
        ('paid', 'Paid')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, default='reserved', choices=TICKET_STATUS)
    ticket_type = models.ForeignKey(TicketType, default=1, on_delete=models.SET_DEFAULT)

    @property
    def price(self):
        return self.ticket_type.price if self.ticket_type else None

    def __str__(self):
        return self.user.username + '_' + self.ticket_type.name

    