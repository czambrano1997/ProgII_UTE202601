from django.db import models

# Create your models here.
# Modelo Clientes
class Clientes(models.Model):
    nombre = models.CharField(max_length=100)
    s_nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    s_apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.IntegerField(verbose_name="Ingresa el telefono")
    fecha_registro = models.DecimalField(auto_created=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Modelo Reservas
class Reservas(models.Model):
    cliente  = models.ForeignKey('clientes' , on_delete=models.CASCADE)
    numero_Rs = models.AutoField(primary_key=True)
    Hora_ll = models.TimeField(auto_now= False,
                                 auto_now_add= False,
                                 null = False,
                                 blank= False,
                                 verbose_name="Hora de llegada"
                                 )
    Hora_Sa = models.TimeField(auto_now= False,
                               auto_now_add= False,
                               null= False,
                               blank= False,
                               verbose_name="Hora de salida")
    Pago = models.DecimalField(max_digits= 10,
                               decimal_places= 2,)
    cantidad_ju = models.IntegerField(verbose_name="Numero de jugadores")
    paquete_incluido = models.ForeignKey('paquete' , on_delete=models.CASCADE,
                                            null= True,
                                            blank= True)
    
    nota = models.TextField(verbose_name="Nota extra de la reservacion")

    def __str__(self):
        return f"{self.cliente}{self.numero_Rs}"
    
# Modelo paquete
class Paquete(models.Model):
    nombre_p = models.CharField(max_length=100)
    costo_p =  models.DecimalField(max_digits=10,
                                   decimal_places=2,
                                   verbose_name="Costo del paquete")
    descripcion = models.TextField(verbose_name="Descripcion del paquete")

    def __str__(self):
        return self.nombre_p
#Modelo invetario
class Inventario(models.Model):
    nombre_p = models.CharField(max_length=100,
                                null=True,
                                blank=True)
    precio_p = models.DecimalField(max_digits=10,
                                   decimal_places=2,
                                   null= True,
                                   blank=True,
                                   verbose_name="Precio unitario")
    cantidad_p = models.IntegerField(verbose_name="Cantidad del producto",
                                    null=True,
                                    blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __set__(self):
        return self.nombre_p

# Modelo gestion de reservas 
class Gestion_reservas(models.Model):
    nombre_cli = models.OneToOneField('cliente',on_delete= models.CASCADE)

    canchas = models.ManyToManyField('Reservas')

    reservo = models.BooleanField(verbose_name="Si resesrvo")

    productos_de_consumo = models.ManyToManyField('inventario')

    def __str__(self):
        return  f"{self.nombre_cli} {self.canchas}"