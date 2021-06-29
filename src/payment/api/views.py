from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from tickets.models import Event, Ticket, TicketType
from payment.api.serializers import TransactionSerializer
from tickets.api.serializers import TicketSerializer
from payment.tools.payment import PaymentGateway, CardError, PaymentError, CurrencyError

class TransactionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, **kwargs):
        context = {
            "request": request,
        }
        token = request.data.pop('token')
        serializer = TransactionSerializer(data=request.data, context=context)
        if serializer.is_valid():
            gateway = PaymentGateway()
            try:
                result = gateway.charge(request.data['amount'], token, request.data['currency'])
            except (CardError, PaymentError, CurrencyError) as error:
                return Response({'Failed': str(error)}, status=status.HTTP_400_BAD_REQUEST)
            transaction = serializer.save()
            ticket = Ticket.objects.get(id=request.data['ticket_id'])
            if ticket is not None:
                ticket.status = 'paid'
                ticket.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, ticket=None):
        queryset = Ticket.objects.all()
        tickets = get_object_or_404(queryset, id=ticket)
        serializer = TicketSerializer(tickets)
        return Response(serializer.data, status=status.HTTP_200_OK)