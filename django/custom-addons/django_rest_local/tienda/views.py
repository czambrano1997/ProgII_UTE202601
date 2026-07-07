from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Producto
from .serializers import ProductoSerializer


@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def lista_productos(request):
    if request.method == "POST":
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    data = serializer.data

    html = """
    <html>
      <head><title>Productos</title></head>
      <body>
        <h1>Productos</h1>
        <p>Usa estas rutas:</p>
        <ul>
          <li><a href="/api/productos/crear/">Crear producto</a></li>
          <li><a href="/api/productos/1/">Ver producto 1</a></li>
          <li><a href="/api/productos/1/" onclick="fetch('/api/productos/1/', {method:'DELETE'}).then(()=>location.reload())">Eliminar producto 1</a></li>
        </ul>
        <pre>{}</pre>
      </body>
    </html>
    """.format(data)
    return HttpResponse(html)


@csrf_exempt
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([AllowAny])
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "GET":
        serializer = ProductoSerializer(producto)
        html = f"""
        <html>
          <head><title>Detalle del producto</title></head>
          <body>
            <h1>Detalle del producto</h1>
            <pre>{escape(str(serializer.data))}</pre>
            <p><a href="/api/productos/">Volver a productos</a></p>
            <p><a href="/api/producto/{pk}/">Ver esta URL singular</a></p>
            <p><button onclick="fetch('/api/productos/{pk}/', {{method:'DELETE'}}).then(()=>alert('Eliminado'))">Eliminar</button></p>
          </body>
        </html>
        """
        return HttpResponse(html)

    if request.method in ["PUT", "PATCH"]:
        serializer = ProductoSerializer(producto, data=request.data, partial=request.method == "PATCH")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    producto.delete()
    return Response({"mensaje": "Producto eliminado correctamente"}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def crear_producto(request):
    if request.method == "POST":
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            producto = serializer.save()
            if request.content_type and "application/json" in request.content_type:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            html = f"""
            <html>
              <head><title>Producto creado</title></head>
              <body>
                <h1>Producto creado correctamente</h1>
                <p>Id: {producto.pk}</p>
                <p><a href="/api/productos/{producto.pk}/">Ver producto</a></p>
                <p><a href="/api/productos/">Volver a productos</a></p>
              </body>
            </html>
            """
            return HttpResponse(html)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    html = """
    <html>
      <head><title>Crear producto</title></head>
      <body>
        <h1>Crear producto</h1>
        <form method="post" action="/api/productos/crear/">
          <label>Nombre</label><br>
          <input type="text" name="nombre"><br><br>
          <label>Precio</label><br>
          <input type="text" name="precio"><br><br>
          <label>Stock</label><br>
          <input type="number" name="stock"><br><br>
          <button type="submit">Guardar</button>
        </form>
        <p><a href="/api/productos/">Volver a productos</a></p>
      </body>
    </html>
    """
    return HttpResponse(html)


@csrf_exempt
@api_view(["PUT", "PATCH"])
@permission_classes([AllowAny])
def actualizar_producto(request, pk):
    return detalle_producto(request, pk)


@csrf_exempt
@api_view(["DELETE"])
@permission_classes([AllowAny])
def eliminar_producto(request, pk):
    return detalle_producto(request, pk)
