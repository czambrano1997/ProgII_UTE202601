from rest_framework import serializers
from peliculas.models import Pelicula, Sala,Funcion,Cliente,Boleto

class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model  =  Pelicula
        fields  = '__all__'

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model  =  Sala
        fields  = '__all__'

class FuncionSerializer(serializers.ModelSerializer):
    class Meta:
        model  =  Funcion
        fields  = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model  =  Cliente
        fields  = '__all__'

class BoletoSerializer(serializers.ModelSerializer):
    class Meta:
        model  =  Boleto
        fields  = '__all__'