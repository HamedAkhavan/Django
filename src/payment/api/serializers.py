from rest_framework import serializers

from payment.models import Transaction
from users.api.serializers import UserSerializer


class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Transaction
        fields = [
            'id',
            'user', 
            'ticket_id', 
            'amount',
            'date',
            'currency',
        ]

