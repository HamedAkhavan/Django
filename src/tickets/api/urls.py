from django.contrib import admin
from django.urls import path
from tickets.api.views import EventViewSet, TicketViewSet, TickeTypetViewSet, TicketQuantityViewSet


urlpatterns = [
    path('events', EventViewSet.as_view({
        'get': 'list',
        'post': 'create',
        })),
    path('<int:event>/ticket_types', TicketQuantityViewSet.as_view({
        'get': 'list',
        'post': 'create',
        })),
    path('<int:event>/tickets', TicketViewSet.as_view({
        'get': 'list',
        'post': 'create',
        })),
    path('ticket_types', TickeTypetViewSet.as_view({'get': 'list'})),
]
