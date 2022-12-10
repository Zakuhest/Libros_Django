from django.contrib import admin
from myapp.models import Alumno, Salon, Cliente, Vendedor, Examen_Final, Proyecto, ProyectoProxy, Profesor

# Register your models here.

admin.site.register(Alumno)
admin.site.register(Salon)
admin.site.register(Cliente)
admin.site.register(Vendedor)
admin.site.register(Examen_Final)
admin.site.register(Profesor)
admin.site.register(Proyecto)
admin.site.register(ProyectoProxy)

