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


class TicketTests(APITestCase):
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
    
    def test_create_event(self):
        url = reverse('tickets-api:events-list')
        data = {
            'name': 'Expo',
            'date': '2021-06-29T12:00:00Z',
            'address': 'dubai',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)

    def test_get_events(self):
        url = reverse('tickets-api:events-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [
            {
                'id': 1,
                'name': 'test',
                'date': '2021-06-29T12:00:00Z',
                'address': 'address',
            }
        ])

    def test_reserve_ticket(self):
        url = reverse('tickets-api:tickets-list', kwargs={'event_pk': 1})
        data = {
            'ticket_type': 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_event_tickets(self):
        url = reverse('tickets-api:tickets-list', kwargs={'event_pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {
                'id': 1,
                'status': 'reserved',
                'ticket_type': 1,
                'price': 20.0
            }
        ])

    def test_add_ticket_type_for_event(self):
        url = reverse('tickets-api:ticket-types-list', kwargs={'event_pk': 1})
        data = {
            'quantity': 40,
            'name': 'Economic',
            'price': 10,
            'event': 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_ticket_types_of_event(self):
        url = reverse('tickets-api:ticket-types-list', kwargs={'event_pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {
                'id': 1,
                'name': 'Regular',
                'price': 20,
                'quantity': 10,
                'event': 1,
            },
            {
                'id': 2,
                'name': 'VIP',
                'price': 40,
                'quantity': 5,
                'event': 1,
            },
        ])

    def test_get_a_ticket_type_of_event(self):
        url = reverse('tickets-api:ticket-types-detail', kwargs={'event_pk': 1, 'pk':1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
                'id': 1,
                'quantity': 10,
                'name': 'Regular',
                'price': 20.0,
                'event': 1
            })
