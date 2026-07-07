from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Autor, Editorial, Categoria, Libro, Prestamo
from .serializers import (AutorSerializer, EditorialSerializer, CategoriaSerializer, 
                          LibroSerializer, PrestamoSerializer)

class AutorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Autores.
    Proporciona endpoints CRUD completos:
    - GET /api/autores/: Lista todos los autores
    - POST /api/autores/: Crea un nuevo autor
    - GET /api/autores/{id}/: Obtiene un autor específico
    - PUT /api/autores/{id}/: Actualiza completamente un autor
    - PATCH /api/autores/{id}/: Actualiza parcialmente un autor
    - DELETE /api/autores/{id}/: Elimina un autor
    """
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class EditorialViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Editoriales.
    Proporciona endpoints CRUD completos.
    """
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Categorías.
    Proporciona endpoints CRUD completos.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class LibroViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Libros.
    Proporciona endpoints CRUD completos:
    - GET /api/libros/: Lista todos los libros
    - POST /api/libros/: Crea un nuevo libro
    - GET /api/libros/{id}/: Obtiene un libro específico
    - PUT /api/libros/{id}/: Actualiza completamente un libro
    - PATCH /api/libros/{id}/: Actualiza parcialmente un libro
    - DELETE /api/libros/{id}/: Elimina un libro
    """
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """Endpoint personalizado para obtener libros por categoría"""
        categoria_id = request.query_params.get('categoria_id')
        if not categoria_id:
            return Response({'error': 'categoria_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        libros = Libro.objects.filter(categoria_id=categoria_id)
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)

class PrestamoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Préstamos.
    Proporciona endpoints CRUD completos:
    - GET /api/prestamos/: Lista todos los préstamos
    - POST /api/prestamos/: Crea un nuevo préstamo
    - GET /api/prestamos/{id}/: Obtiene un préstamo específico
    - PUT /api/prestamos/{id}/: Actualiza completamente un préstamo
    - PATCH /api/prestamos/{id}/: Actualiza parcialmente un préstamo
    - DELETE /api/prestamos/{id}/: Elimina un préstamo
    """
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Endpoint personalizado para obtener préstamos activos"""
        prestamos_activos = Prestamo.objects.filter(estado='activo')
        serializer = self.get_serializer(prestamos_activos, many=True)
        return Response(serializer.data)