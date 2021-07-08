from rest_framework import serializers

from tickets.models import Ticket, TicketType, Event
from users.api.serializers import UserSerializer


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = [
            'id',
            'name',
            'quantity',
            'event',
            'price',
        ]

class TicketSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    price = serializers.ReadOnlyField()
    class Meta:
        model = Ticket
        fields = [
            'id',
            'user', 
            'status',
            'ticket_type',
            'price',
        ]



class EventSerializer(serializers.ModelSerializer):
    # tickets = TicketSerializer(read_only=True, many=True)
    available_ticket = serializers.ReadOnlyField()

    class Meta:
        ordering = ['-date']
        model = Event
        # depth = 1
        fields = [
            'id',
            'name',
            'date', 
            'address',
            'available_ticket',
        ]
