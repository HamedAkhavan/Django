from django.contrib import admin
from django.urls import path
from payment.api.views import TransactionViewSet


urlpatterns = [
    path('<int:ticket>/pay', TransactionViewSet.as_view({
        'get': 'retrieve',
        'post': 'create',
        }
    )),
]
