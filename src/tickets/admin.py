from django.contrib import admin
from tickets.models import Ticket, Event, TicketType, TicketQuantity
# Register your models here.
class TicketTypeAdmin(admin.ModelAdmin):
    pass

class TicketAdmin(admin.ModelAdmin):
    pass
class TicketQuantityInline(admin.TabularInline):
    model = TicketQuantity
class EventAdmin(admin.ModelAdmin):
    inlines = [
        TicketQuantityInline,
    ]



admin.site.register(Ticket, TicketAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(TicketType, TicketTypeAdmin)