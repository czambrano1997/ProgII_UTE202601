from rest_framework import serializers
from .models import Autor, Editorial, Categoria, Libro, Prestamo

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'apellido', 'fecha_nacimiento']

class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = ['id', 'nombre', 'pais']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']

class LibroSerializer(serializers.ModelSerializer):
    autor_nombre = serializers.CharField(source='autor.nombre', read_only=True)
    editorial_nombre = serializers.CharField(source='editorial.nombre', read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor', 'autor_nombre', 'editorial', 'editorial_nombre', 
                  'categoria', 'categoria_nombre', 'isbn', 'fecha_publicacion', 'paginas']
    
    def validate_paginas(self, value):
        if value <= 0:
            raise serializers.ValidationError("Las páginas deben ser mayor que 0")
        return value

class PrestamoSerializer(serializers.ModelSerializer):
    libro_titulo = serializers.CharField(source='libro.titulo', read_only=True)
    
    class Meta:
        model = Prestamo
        fields = ['id', 'libro', 'libro_titulo', 'usuario', 'fecha_prestamo', 
                  'fecha_devolucion_esperada', 'fecha_devolucion_real', 'estado']