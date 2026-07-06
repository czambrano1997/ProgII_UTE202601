from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Producto
from .serializers import ProductoSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def lista_productos(request):
    productos = Producto.objects.all()          
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    serializer = ProductoSerializer(producto)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def crear_producto(request):
    serializer = ProductoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticatedOrReadOnly])
def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    serializer = ProductoSerializer(producto, data=request.data, partial=request.method == "PATCH")
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return Response({"mensaje": "Producto eliminado correctamente"}, status=status.HTTP_200_OK)
