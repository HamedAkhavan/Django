import time
from celery.decorators import task
from tickets.models import Ticket

@task(name="delete_ticket_after_15")
def delete_ticket(id):
    time.sleep(900)
    ticket = Ticket.objects.get(id=id)
    if ticket.status == 'reserved':
        ticket.delete()

