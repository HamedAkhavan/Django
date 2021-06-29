from django.contrib import admin
from django.urls import path
from tickets.api.views import EventViewSet, TicketViewSet, TickeTypetViewSet, TicketQuantityViewSet


urlpatterns = [
    path('events', EventViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }), name='events'),
    path('<int:event>/ticket-types', TicketQuantityViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }), name='event-ticket-types'),
    path('<int:event>/ticket-types/<int:ticket_type>', TicketQuantityViewSet.as_view({
            'get': 'retrieve',
        }), name='event-ticket-type'),
    path('<int:event>/tickets', TicketViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }), name='tickets'),
    path('ticket_types', TickeTypetViewSet.as_view({
            'get': 'list'
        }), name='ticket-types'),
]
