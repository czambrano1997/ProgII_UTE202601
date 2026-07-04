from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Cliente, Reserva, Paquete, Inventario, Canchas
from .serializers import (
    ClienteSerializer,
    ReservaSerializer,
    PaqueteSerializer,
    InventarioSerializer,
    CanchasSerializer,
)


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [AllowAny]


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [AllowAny]


class PaqueteViewSet(viewsets.ModelViewSet):
    queryset = Paquete.objects.all()
    serializer_class = PaqueteSerializer
    permission_classes = [AllowAny]


class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    permission_classes = [AllowAny]


class CanchasViewSet(viewsets.ModelViewSet):
    queryset = Canchas.objects.all()
    serializer_class = CanchasSerializer
    permission_classes = [AllowAny]
