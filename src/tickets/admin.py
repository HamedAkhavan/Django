from django.contrib import admin
from tickets.models import Ticket, Event, TicketType
# Register your models here.
class TicketTypeInline(admin.TabularInline):
    model = TicketType

class TicketAdmin(admin.ModelAdmin):
    pass
class EventAdmin(admin.ModelAdmin):
    inlines = [
        TicketTypeInline,
    ]



admin.site.register(Ticket, TicketAdmin)
admin.site.register(Event, EventAdmin)