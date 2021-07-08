from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from tickets.models import Event, Ticket, TicketType
from tickets.api.serializers import EventSerializer, TicketSerializer, TicketTypeSerializer
from tickets.tasks import delete_ticket
class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def list(self, request, event_pk=None):
        event = Event.objects.get(pk=event_pk)
        ticket_type = TicketType.objects.filter(event=event)
        if request.user.is_superuser:
            tickets = get_list_or_404(self.queryset, ticket_type__in=ticket_type)
        else:
            tickets = get_list_or_404(self.queryset, ticket_type__in=ticket_type, user=request.user)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request, event_pk=None):
        context = {
            "request": request,
        }
        serializer = TicketSerializer(data=request.data, context=context)
        if serializer.is_valid() and 'ticket_type' in request.data:
            event = Event.objects.get(pk=event_pk)
            ticket_type = TicketType.objects.get(id=request.data['ticket_type'])
            if ticket_type.remaining>0:
                ticket = serializer.save(ticket_type = ticket_type)
                ticket.save()
                delete_ticket.delay(ticket.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'Failed: No tickets available for this ticket type'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
# class TickeTypetViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
#     queryset = TicketType.objects.all()
#     serializer_class = TicketTypeSerializer
    
class TicketTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
    
    def list(self, request, event_pk=None):
        event = Event.objects.get(pk=event_pk)
        ticket_types = get_list_or_404(self.queryset, event=event_pk)
        serializer = TicketTypeSerializer(ticket_types, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def retrieve(self, request, event_pk=None, pk=None):
        ticket_quantity = get_object_or_404(self.queryset, id=pk)
        serializer = TicketTypeSerializer(ticket_quantity)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def create(self, request, event_pk=None):
        serializer = TicketTypeSerializer(data=request.data)
        if serializer.is_valid():
            event = Event.objects.get(pk=event_pk)
            serializer.save(event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)