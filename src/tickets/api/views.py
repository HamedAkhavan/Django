from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from tickets.models import Event, Ticket, TicketType, TicketQuantity
from tickets.api.serializers import EventSerializer, TicketSerializer, TicketTypeSerializer, TicketQuantitySerializer
from tickets.tasks import delete_ticket
class EventViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny, ]


    def list(self, request):
        queryset = Event.objects.all()
        events = get_list_or_404(queryset)
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class TicketViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, event=None):
        queryset = Ticket.objects.all()
        tickets = get_list_or_404(queryset, event_id=event, user=request.user)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request, event=None):
        context = {
            "request": request,
        }
        serializer = TicketSerializer(data=request.data, context=context)
        if serializer.is_valid():
            event = Event.objects.get(pk=event)
            ticket_type_name = TicketType.objects.get(id=request.data['ticket_type']).name
            if event.available_ticket[ticket_type_name]>0:
                ticket = serializer.save(event_id = event)
                ticket.save()
                delete_ticket.delay(ticket.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'Failed: No tickets available for this ticket type'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
class TickeTypetViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    
    def list(self, request, event=None):
        queryset = TicketType.objects.all()
        ticket_types = get_list_or_404(queryset)
        serializer = TicketTypeSerializer(ticket_types)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def create(self, request):
        serializer = TicketTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class TicketQuantityViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    
    def list(self, request, event=None):
        queryset = TicketQuantity.objects.all()
        event = Event.objects.get(pk=event)
        ticket_types = get_list_or_404(queryset, event_id=event)
        serializer = TicketQuantitySerializer(ticket_types)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def create(self, request, event=None):
        serializer = TicketQuantitySerializer(data=request.data)
        if serializer.is_valid():
            event = Event.objects.get(pk=event)
            serializer.save(event_id=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)