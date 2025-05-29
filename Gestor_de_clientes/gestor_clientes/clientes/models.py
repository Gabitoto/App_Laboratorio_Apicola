from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=150, db_comment='Correo electronico del cliente')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True, db_comment='Fecha y hora de registro del cliente')
    activo = models.BooleanField(blank=True, null=True, db_comment='Estado del cliente (activo/inactivo)')
    notas = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cliente'
        db_table_comment = 'Tabla para almacenar informacion de clientes'
