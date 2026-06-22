from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Producto, Pedido, DetallePedido
from .forms import PerfilForm, RegistroCompletoForm
from decimal import Decimal
from django.utils import timezone
from django.utils.timezone import localtime
from django.db.models import Sum, Avg, Count, Max, Value
from django.db.models.functions import Concat

# --- IMPORTACIONES PARA APIS ---
from django.http import JsonResponse

# Función auxiliar para verificar roles
def es_vendedor(user):
    return user.is_staff

def es_admin(user):
    return user.is_superuser

# --- 1. VISTAS DE CATÁLOGO (FILTRADAS PARA OCULTAR AGOTADOS) ---

def lista_productos(request):
    # Solo mostramos productos disponibles para el cliente
    productos = Producto.objects.filter(disponible=True).order_by('nombre')
    return render(request, 'lista_productos.html', {
        'productos': productos, 
        'titulo': 'Nuestra Vitrina'
    })

def catalogo_panaderia(request):
    productos = Producto.objects.filter(categoria='PAN', disponible=True).order_by('nombre')
    return render(request, 'lista_productos.html', {
        'productos': productos, 
        'titulo': 'Sección Panadería'
    })

def catalogo_pasteleria(request):
    productos = Producto.objects.filter(categoria='PAS', disponible=True).order_by('nombre')
    return render(request, 'lista_productos.html', {
        'productos': productos, 
        'titulo': 'Sección Pastelería'
    })

def catalogo_postres(request):
    productos = Producto.objects.filter(categoria='POS', disponible=True).order_by('nombre')
    return render(request, 'lista_productos.html', {
        'productos': productos, 
        'titulo': 'Sección Postres'
    })


# --- 2. GESTIÓN DE CARRITO Y COMPRAS (MODIFICADO PARA MÚLTIPLES CANTIDADES) ---

@login_required 
def agregar_al_pedido(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Capturamos la cantidad enviada por el usuario (desde el catálogo)
    try:
        cantidad_a_comprar = int(request.POST.get('cantidad', 1))
    except ValueError:
        cantidad_a_comprar = 1

    # Verificación de Seguridad: No agregar si no hay stock o está oculto
    if not producto.disponible or producto.stock < cantidad_a_comprar:
        messages.error(request, f'Lo sentimos, solo quedan {producto.stock} unidades de {producto.nombre}.')
        return redirect('lista_productos')
    
    pedido, created = Pedido.objects.get_or_create(cliente=request.user, completado=False)
    if created or pedido.total is None:
        pedido.total = Decimal('0.00')
    
    detalle, _ = DetallePedido.objects.get_or_create(
        pedido=pedido, producto=producto,
        defaults={'cantidad': 0, 'precio_unitario': producto.precio}
    )
    
    # Actualizamos cantidad en el detalle
    detalle.cantidad += cantidad_a_comprar
    detalle.save()
    
    # Actualizamos el total del pedido
    monto_a_sumar = Decimal(str(producto.precio)) * cantidad_a_comprar
    pedido.total = Decimal(str(pedido.total)) + monto_a_sumar
    pedido.save()
    
    # Resta stock según la cantidad elegida
    producto.stock -= cantidad_a_comprar
    if producto.stock == 0:
        producto.disponible = False
    producto.save()
    
    messages.success(request, f'Has añadido {cantidad_a_comprar} unidades de {producto.nombre} al carrito.')
    return redirect('lista_productos')

@login_required
def ver_carrito(request):
    pedido = Pedido.objects.filter(cliente=request.user, completado=False).first()
    detalles = DetallePedido.objects.filter(pedido=pedido).order_by('id') if pedido else []
    
    ultimo_pedido = Pedido.objects.filter(cliente=request.user, completado=True).last()
    telefono_sugerido = ultimo_pedido.telefono if ultimo_pedido and ultimo_pedido.telefono else ""
    
    return render(request, 'carrito.html', {
        'pedido': pedido, 
        'detalles': detalles,
        'telefono_sugerido': telefono_sugerido 
    })
   
@login_required
def eliminar_del_carrito(request, detalle_id):
    detalle = get_object_or_404(DetallePedido, id=detalle_id, pedido__cliente=request.user)
    pedido = detalle.pedido
    producto = detalle.producto
    
    pedido.total = max(Decimal(str(pedido.total)) - Decimal(str(detalle.precio_unitario)), Decimal('0.00'))
    pedido.save()
    
    # Al eliminar del carrito, devolvemos el stock al inventario
    producto.stock += 1
    if producto.stock > 0:
        producto.disponible = True
    producto.save()

    if detalle.cantidad > 1:
        detalle.cantidad -= 1
        detalle.save()
    else:
        detalle.delete()
    return redirect('ver_carrito')

@login_required
def finalizar_compra(request):
    if request.method == 'POST':
        pedido = Pedido.objects.filter(cliente=request.user, completado=False).first()
        
        if not pedido or not DetallePedido.objects.filter(pedido=pedido).exists():
            messages.error(request, "Tu carrito está vacío.")
            return redirect('lista_productos')

        tel = request.POST.get('telefono')
        if tel:
            pedido.telefono = tel
        
        # --- LÓGICA DE CÓDIGO MANUAL SOLO PARA PASTELERÍA ('PAS') ---
        codigo_promo = request.POST.get('codigo_descuento', '').strip().upper()
        
        if codigo_promo == "IDEAL2026":
            descuento_pasteleria = Decimal('0.00')
            detalles_carrito = DetallePedido.objects.filter(pedido=pedido)
            encontro_pasteles = False

            for item in detalles_carrito:
                if item.producto.categoria == 'PAS':
                    ahorro_item = (item.precio_unitario * item.cantidad) * Decimal('0.20')
                    descuento_pasteleria += ahorro_item
                    encontro_pasteles = True

            if encontro_pasteles:
                pedido.total -= descuento_pasteleria
                messages.success(request, f'¡Código IDEAL2026 aplicado! Ahorraste ${descuento_pasteleria} en tus pasteles.')
            else:
                messages.warning(request, 'El código IDEAL2026 es válido pero solo aplica para la categoría Pastelería.')

        # --- Lógica de Puntos ---
        pedidos_anteriores = Pedido.objects.filter(cliente=request.user, completado=True)
        total_historico = sum(p.total for p in pedidos_anteriores)
        puntos_totales = int(total_historico / 10)
        
        if puntos_totales >= 7:
            descuento_puntos = pedido.total * Decimal('0.10')
            pedido.total -= descuento_puntos
            messages.success(request, '¡Puntos Canjeados! Descuento de 10% aplicado.')
        
        pedido.completado = True
        pedido.estado = 'Pendiente' 
        pedido.save()
        
        messages.success(request, f'¡Gracias por elegir La Ideal! Te contactaremos al {tel}.')
        return redirect('lista_productos')
    
    return redirect('ver_carrito')


# --- 3. ÁREA DE USUARIO Y PERFIL ---

def registro(request):
    if request.method == 'POST':
        form = RegistroCompletoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cuenta creada con éxito!')
            return redirect('login')
    else:
        form = RegistroCompletoForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user, completado=True).order_by('-fecha_pedido')
    return render(request, 'mis_pedidos.html', {'pedidos': pedidos})

@login_required
def perfil_usuario(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Datos actualizados!')
            return redirect('perfil_usuario')
    else:
        form = PerfilForm(instance=request.user)

    pedidos_finalizados = Pedido.objects.filter(cliente=request.user, completado=True).order_by('-fecha_pedido')
    datos_agregados = pedidos_finalizados.aggregate(Sum('total'))
    total_gastado = datos_agregados['total__sum'] or Decimal('0.00')
    puntos_totales = int(total_gastado / 10)
    meta_puntos = 500
    puntos_porcentaje = min(int((puntos_totales / meta_puntos) * 100), 100)
    
    if puntos_totales < 50:
        rango = "Iniciado en el Trigo 🥖"
    elif puntos_totales < 200:
        rango = "Amante del Dulce 🍰"
    else:
        rango = "Leyenda de La Ideal 👑"
        
    return render(request, 'perfil.html', {
        'form': form, 
        'puntos': puntos_totales, 
        'puntos_porcentaje': puntos_porcentaje, 
        'rango': rango,
        'pedidos': pedidos_finalizados, 
        'total_pedidos': pedidos_finalizados.count(), 
        'total_gastado': round(total_gastado, 2),
        'faltan_puntos': max(0, meta_puntos - puntos_totales)
    })


# --- 4. GESTIÓN DEL VENDEDOR (VENTAS Y MERMAS) ---

@login_required
@user_passes_test(es_vendedor)
def panel_vendedor(request):
    hoy = localtime().date()
    pedidos_pendientes = Pedido.objects.filter(completado=True, estado='Pendiente').order_by('-fecha_pedido')
    ventas_hoy = Pedido.objects.filter(estado='Entregado', fecha_pedido__date=hoy)
    total_raw = ventas_hoy.aggregate(Sum('total'))['total__sum'] or Decimal('0.00')
    total_caja = round(total_raw, 2) 
    productos = Producto.objects.all().order_by('stock')

    return render(request, 'panel_vendedor.html', {
        'pedidos': pedidos_pendientes, 
        'ventas_hoy': ventas_hoy,
        'total_caja': total_caja, 
        'productos': productos
    })

@login_required
@user_passes_test(es_vendedor)
def entregar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = 'Entregado' 
    pedido.save()
    messages.success(request, f'Pedido #{pedido_id} entregado. Stock sincronizado.')
    return redirect('panel_vendedor')

@login_required
@user_passes_test(es_vendedor)
def toggle_stock(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.disponible = not producto.disponible
    if producto.disponible and producto.stock <= 0:
        producto.stock = 15
    producto.save()
    return redirect('panel_vendedor')

@login_required
@user_passes_test(es_vendedor)
def venta_rapida(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if producto.stock <= 0:
        messages.error(request, f"No hay stock de {producto.nombre}.")
        return redirect('panel_vendedor')

    cliente_mostrador, _ = User.objects.get_or_create(username='Consumidor_Final')
    pedido = Pedido.objects.create(
        cliente=cliente_mostrador,
        total=producto.precio,
        completado=True,
        estado='Entregado'
    )
    DetallePedido.objects.create(
        pedido=pedido, producto=producto,
        cantidad=1, precio_unitario=producto.precio
    )
    producto.stock -= 1
    producto.save()
    messages.success(request, f"⚡ Venta rápida registrada: {producto.nombre}.")
    return redirect('panel_vendedor')

@login_required
@user_passes_test(es_vendedor)
def registrar_merma(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if producto.stock > 0:
        producto.stock -= 1
        if producto.stock == 0:
            producto.disponible = False
        producto.save()
        messages.warning(request, f"Se descontó 1 unidad de {producto.nombre} por merma.")
    else:
        messages.error(request, "No hay stock para descontar merma.")
    return redirect('panel_vendedor')


# --- 5. IMPRIMIR TICKET ---
@login_required
@user_passes_test(es_vendedor)
def imprimir_ticket(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    return render(request, 'ticket_preparacion.html', {
        'pedido': pedido,
        'detalles': detalles,
        'fecha': timezone.now()
    })

# --- 6. APIS (MEJORADO PARA MENSAJE DE ENTREGA) ---

def api_buscar_productos(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=query, disponible=True, stock__gt=0)[:12]
    datos = []
    for p in productos:
        datos.append({
            'id': p.id,
            'nombre': p.nombre,
            'precio': str(p.precio),
            'imagen': p.imagen.url if p.imagen else '/static/default.jpg',
            'categoria': p.get_categoria_display(),
            'stock': p.stock 
        })
    return JsonResponse(datos, safe=False)

def api_estado_pedido(request):
    if request.user.is_authenticated:
        # Buscamos el último pedido completado para avisar al usuario
        ultimo_pedido = Pedido.objects.filter(cliente=request.user, completado=True).order_by('-fecha_pedido').first()
        if ultimo_pedido:
            # Si el estado es 'Entregado', enviamos el mensaje de éxito
            return JsonResponse({
                'id': ultimo_pedido.id,
                'estado': ultimo_pedido.estado,
                'mensaje': f'¡Tu pedido #{ultimo_pedido.id} ha sido entregado con éxito! Gracias por preferir La Ideal.' if ultimo_pedido.estado == 'Entregado' else 'Tu pedido está en preparación.'
            })
    return JsonResponse({'estado': 'ninguno'})


# --- 7. PANEL DE CONTROL MAESTRO (ADMINISTRADOR) ---

@login_required
@user_passes_test(es_admin)
def dashboard_admin(request):
    # 1. Agregaciones SQL 
    ventas_totales = Pedido.objects.filter(completado=True).aggregate(Sum('total'))['total__sum'] or 0
    promedio_venta = Pedido.objects.filter(completado=True).aggregate(Avg('total'))['total__avg'] or 0
    conteo_pedidos = Pedido.objects.filter(completado=True).count()
    max_venta = Pedido.objects.filter(completado=True).aggregate(Max('total'))['total__max'] or 0
    
    # 2. Listado de Usuarios con Concatenación de Nombre
    usuarios = User.objects.annotate(
        nombre_completo=Concat('first_name', Value(' '), 'last_name')
    ).order_by('-date_joined')

    # 3. teléfonos únicos
    contactos = Pedido.objects.filter(
        completado=True
    ).exclude(
        telefono__isnull=True
    ).exclude(
        telefono=''
    ).values('cliente__username', 'telefono').distinct().order_by('cliente__username')

    # 4. Inventario
    todos_los_productos = Producto.objects.all().order_by('nombre')
    alerta_stock = Producto.objects.filter(stock__lte=5).order_by('stock')

    # 5. TOP 5 PRODUCTOS
    top_productos = DetallePedido.objects.filter(
        pedido__completado=True
    ).values('producto__nombre').annotate(
        total_vendido=Sum('cantidad')
    ).order_by('-total_vendido')[:5]

    return render(request, 'admin_dashboard.html', {
        'total_dinero': round(ventas_totales, 2),
        'promedio': round(promedio_venta, 2),
        'cantidad_pedidos': conteo_pedidos,
        'venta_record': max_venta,
        'usuarios': usuarios,
        'contactos': contactos, 
        'productos_alerta': alerta_stock,
        'todos_productos': todos_los_productos,
        'top_productos': top_productos,
        'titulo': "Dashboard Maestro - La Ideal"
    })

@login_required
@user_passes_test(es_admin)
def admin_reabastecer(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = int(request.POST.get('cantidad', 0))
        
        if cantidad > 0:
            producto.stock += cantidad
            if producto.stock > 0:
                producto.disponible = True 
            producto.save()
            messages.success(request, f"¡Éxito! Se cargaron {cantidad} unidades de {producto.nombre}.")
        else:
            messages.warning(request, "Escribe una cantidad válida.")
            
    return redirect('dashboard_admin') 

# --- 8. DETALLE DE COMPRA PARA EL USUARIO ---

@login_required
def detalle_pedido(request, pedido_id):
    # Obtenemos el pedido asegurando que sea del usuario logueado
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user, completado=True)
    
    # Obtenemos los detalles (productos comprados) de ese pedido
    detalles = DetallePedido.objects.filter(pedido=pedido).select_related('producto')
    
    return render(request, 'detalle_pedido.html', {
        'pedido': pedido,
        'detalles': detalles,
        'titulo': f'Resumen de Pedido #{pedido.id}'
    })