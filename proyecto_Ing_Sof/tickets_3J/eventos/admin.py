from django.contrib import admin
from .models import Evento, Reserva, Boleta, Localidad, EventoLocalidad



admin.site.register(Boleta)
admin.site.register(Reserva)
admin.site.register(Evento)
admin.site.register(Localidad)
admin.site.register(EventoLocalidad)
