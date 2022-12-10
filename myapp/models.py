from django.db import models
from datetime import date

class Salon(models.Model):
    aula = models.CharField(max_length=2)
    hora_entrada = models.TimeField()

    def full_name(self):
        return self.aula

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    idSalon = models.ForeignKey(Salon, on_delete = models.CASCADE)

    def full_name(self):
        return self.first_name + " " + self.last_name

    class Meta:
        abstract = True

class Alumno(Person):
    nota_laboratorio = models.FloatField(default=0.0)
    examen = models.FloatField(default=0.0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['id', 'first_name', 'last_name'], name = 'primary_key_alumno'
            )
        ]

class Profesor(Person):
    salario = models.FloatField(default=0.0)
    rating = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['id', 'first_name', 'last_name'], name = 'primary_key_profesor'
            )
        ]

class infoPersona(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=9)

    class Meta:
        abstract=True

class Cliente(infoPersona):
    descuento = models.FloatField()

class Vendedor(infoPersona):
    sueldo = models.FloatField()

class Evaluacion(models.Model):
    class Meta:
        abstract=True

    hora_fecha=models.DateField(auto_now=True)
    curso=models.CharField(max_length=30)
    evaluador=models.CharField(max_length=50)

class Examen_Final(Evaluacion):
    duracion_examen = models.DateField(auto_now=True)
    n_preguntas = models.IntegerField(default=0)
    puntaje_total = models.FloatField(default=0.0)

    def puntaje_por_pregunta(self):
        return self.n_preguntas / self.puntaje_total

class Proyecto(Evaluacion):
    tema = models.CharField(max_length=100)
    n_grupos = models.IntegerField(default=0)

class ProyectoProxy(Proyecto):
    class Meta:
        proxy=True
        ordering=['tema']

class Libro(models.Model):
    title=models.TextField(max_length=250)
    authors=models.TextField(max_length=250)
    average_rating=models.FloatField(default=0.0)
    isbn=models.CharField(max_length=20)
    isbn13=models.CharField(max_length=20)
    language_code=models.CharField(max_length=10)
    num_pages=models.IntegerField()
    ratings_count=models.IntegerField()
    text_reviews_count=models.IntegerField()
    publication_date=models.DateField()
    publisher=models.TextField(max_length=250)