from django.contrib import admin
from django.urls import path, include  # 1. Agregamos 'include'
from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views 
from ventas import views 

# 2. Importamos el router de DRF
from rest_framework.routers import DefaultRouter

# 3. Configuramos el router
router = DefaultRouter()
router.register(r'productos', views.ProductoViewSet)
router.register(r'pedidos', views.PedidoViewSet)
router.register(r'detalle-pedidos', views.DetallePedidoViewSet)
router.register(r'usuarios', views.UserViewSet)
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')

urlpatterns = [
    # --- ADMIN Y PÁGINA PRINCIPAL ---
    path('admin/', admin.site.urls), 
    path('', views.lista_productos, name='lista_productos'),

    # --- CATEGORÍAS ---
    path('panaderia/', views.catalogo_panaderia, name='panaderia'),
    path('pasteleria/', views.catalogo_pasteleria, name='pasteleria'),
    path('postres/', views.catalogo_postres, name='catalogo_postres'),

    # --- ÁREA DE USUARIO ---
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),

    # --- COMPRAS ---
    path('comprar/<int:producto_id>/', views.agregar_al_pedido, name='agregar_al_pedido'),
    path('pedido/agregar/<int:producto_id>/', views.agregar_al_pedido), 

    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('eliminar-item/<int:detalle_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),

    # --- GESTIÓN VENDEDOR ---
    path('gestion-ventas/', views.panel_vendedor, name='panel_vendedor'),
    path('entregar/<int:pedido_id>/', views.entregar_pedido, name='entregar_pedido'),
    path('toggle-stock/<int:producto_id>/', views.toggle_stock, name='toggle_stock'),
    path('venta-rapida/<int:producto_id>/', views.venta_rapida, name='venta_rapida'),
    path('merma/<int:producto_id>/', views.registrar_merma, name='registrar_merma'),
    path('imprimir-ticket/<int:pedido_id>/', views.imprimir_ticket, name='imprimir_ticket'),

    # --- GESTIÓN ADMINISTRADOR ---
    path('control-maestro/', views.dashboard_admin, name='dashboard_admin'),
    path('admin-reabastecer/<int:producto_id>/', views.admin_reabastecer, name='admin_reabastecer'),

    # --- APIS ---
    path('api/buscar/', views.api_buscar_productos, name='api_buscar'),
    path('api/estado-pedido/', views.api_estado_pedido, name='api_estado_pedido'),
    
    # 4. AGREGAMOS LAS RUTAS DE LOS VIEWSETS (API REST)
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)