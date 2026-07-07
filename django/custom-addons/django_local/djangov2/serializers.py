from rest_framework import serializers

from .models import Autor, Categoria, Libro, Prestamo, Usuario


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = "__all__"


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = "__all__"


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"


class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = "__all__"
