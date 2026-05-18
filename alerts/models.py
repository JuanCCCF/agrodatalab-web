from django.db import models

# Create your models here.
class Alert(models.Model):

    TIPO_CHOICES = [
        ("Sequedad", "sequedad"),
        ("Temperatura incoherente", "temperatura incoherente"),
        ("Energía baja", "energia baja"),
    ]

    NIVEL_CHOICES = [
        ("bajo", "Baja"),
        ("medio", "Media"),
        ("alto", "Alta"),
        ("critico", "Crítico"),
    ]

    VARIABLE_CHOICES = [
        ("humedad", "Humedad"),
        ("temperatura", "Temperatura"),
        ("bateria", "Batería"),
    ]

    fecha = models.DateTimeField(auto_now_add=True)

    tipo = models.CharField(
        max_length=30,
        choices=TIPO_CHOICES,
    )

    nivel = models.CharField(
        max_length=20,
        choices=NIVEL_CHOICES
    )
    descripcion = models.TextField()
    
    variable_afectada = models.CharField(
        max_length=20,
        choices=VARIABLE_CHOICES,
        editable=False
    )

    def save(self, *args, **kwargs):

        mapa_variable = {
            "Sequedad": "humedad",
            "Temperatura incoherente": "temperatura",
            "Energía baja": "bateria",
        }

        self.variable_afectada = mapa_variable.get(self.tipo)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo} - {self.nivel}"


class Recommendation(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("revisada", "Revisada"),
        ("descartada", "Descartada"),
    ]

    PRIORIDAD_CHOICES = [
        ("baja", "Baja"),
        ("media", "Media"),
        ("alta", "Alta"),
        ("critica", "Crítica"),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    alerta = models.ForeignKey(
        Alert,
        on_delete=models.CASCADE,
        related_name="recomendaciones"
    )

    prioridad = models.CharField(
        max_length=20,
        choices=PRIORIDAD_CHOICES,
        default="media"
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente"
    )

    def __str__(self):
        return self.titulo