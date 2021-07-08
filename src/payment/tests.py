import time
import datetime
import pytz
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from tickets.models import TicketType, Event, Ticket
from payment.models import Transaction


class PaymentTests(APITestCase):

    def setUp(self):
        user = User.objects.create_user('john', 'john@example.com', '123456')
        self.client.login(username='john', password='123456')
        event = Event.objects.create(name='test', date='2021-06-29T12:00:00Z', address='address')
        ticket_type_1 = TicketType.objects.create(
            name='Regular', 
            event=event,
            price=20,
            quantity=10,
        )
        ticket_type_2 = TicketType.objects.create(
            name='VIP', 
            event=event,
            price=40,
            quantity=5,
        )
        ticket = Ticket.objects.create(user=user, ticket_type=ticket_type_1)

    def test_payment(self):
        url = reverse('payment-api:pay', kwargs={'ticket':1})
        data = {
            'ticket_id': 1, 
            'amount': 20,
            'currency': 'EUR',
            'token': 'card_info_customer_info_order_info'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Ticket.objects.get().status, 'paid')
        self.assertEqual(Transaction.objects.count(), 1)