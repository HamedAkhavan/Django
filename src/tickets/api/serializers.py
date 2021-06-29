from rest_framework import serializers

from tickets.models import Ticket, TicketType, TicketQuantity, Event
from users.api.serializers import UserSerializer


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = [
            'id',
            'name',
        ]

class TicketQuantitySerializer(serializers.ModelSerializer):
    remaining = serializers.ReadOnlyField()
    class Meta:
        model = TicketQuantity
        fields = [
            'id',
            'quantity',
            'ticket_type',
            'price',
            'remaining',
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
            'event_id', 
            'status',
            'ticket_type',
            'price',
        ]
        extra_kwargs = {
            'event_id': {'required': False},
        }



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
