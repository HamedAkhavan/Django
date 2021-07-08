from django.contrib import admin
from django.urls import path, include
from tickets.api.views import EventViewSet, TicketViewSet, TicketTypeViewSet
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r'events', EventViewSet, 'events')


ticket_type_router = routers.NestedSimpleRouter(router, r'events', lookup='event')
ticket_router = routers.NestedSimpleRouter(router, r'events', lookup='event')

ticket_type_router.register(r'ticket-types', TicketTypeViewSet, 'ticket-types')
ticket_router.register(r'tickets', TicketViewSet, 'tickets')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(ticket_type_router.urls)),
    path('', include(ticket_router.urls)),
]

# urlpatterns = router.urls

# urlpatterns = [
#     path('events', EventViewSet.as_view({
#             'get': 'list',
#             'post': 'create',
#         }), name='events'),
#     path('events/<int:event>/ticket-types', TickeTypetViewSet.as_view({
#             'get': 'list',
#             'post': 'create',
#         }), name='event-ticket-types'),
#     path('events/<int:event>/tickets', TicketViewSet.as_view({
#             'get': 'list',
#             'post': 'create',
#         }), name='tickets'),
# ]
