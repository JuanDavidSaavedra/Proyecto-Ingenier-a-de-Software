from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from eventos.models import Evento, Localidad, EventoLocalidad
from .models import Compra



@login_required
def comprar_boletas(request, evento_id):
    # Obtenemos el evento relacionado
    evento = get_object_or_404(Evento, id=evento_id)
    
    # Obtenemos las localidades disponibles para este evento
    localidades = EventoLocalidad.objects.filter(evento=evento)

    if request.method == 'POST':
        # Procesar la compra de boletas
        cantidad = int(request.POST.get('cantidad', 1))
        localidad_id = request.POST.get('localidad')  # Localidad seleccionada
        localidad = get_object_or_404(Localidad, id=localidad_id)

        # Verificar si la cantidad solicitada está disponible en la localidad seleccionada
        evento_localidad = EventoLocalidad.objects.get(evento=evento, localidad=localidad)

        # Verificar el total de boletas compradas por el usuario para este evento
        compras_usuario = Compra.objects.filter(usuario=request.user, evento=evento)
        total_comprado = sum(compra.cantidad for compra in compras_usuario)

        if total_comprado + cantidad > 10:
            # Si el total de boletas compradas supera 10, mostramos un mensaje de error
            messages.error(request, f'No puedes comprar más de 10 boletas en total para este evento.')
            return redirect('comprar_boletas', evento_id=evento_id)

        if cantidad <= evento_localidad.boletas_disponibles:
            # Descontar las boletas de la localidad
            evento_localidad.boletas_disponibles -= cantidad
            evento_localidad.save()

            # Crear la compra
            compra = Compra.objects.create(usuario=request.user, evento=evento, cantidad=cantidad)

            # Mensaje de éxito
            messages.success(request, f'Compra exitosa: {cantidad} boletas para {evento.nombre} en la localidad {localidad.nombre}.')
            
            # Redirige a la página de eventos o a donde desees
            return redirect('comprar_boletas', evento_id=evento_id)

        else:
            # Si no hay suficientes boletos disponibles, mensaje de error
            messages.error(request, f'No hay suficientes boletas disponibles para la localidad {localidad.nombre}.')
            return redirect('comprar_boletas', evento_id=evento_id)

    # Pasar las localidades disponibles y mostrar la página
    return render(request, 'comprar_boletas.html', {'evento': evento, 'localidades': localidades})

def confirmar_compra(request, evento_id):
    # Lógica para confirmar la compra
    return render(request, 'boletas/confirmar_compra.html', {'evento_id': evento_id})