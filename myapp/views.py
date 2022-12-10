from django.shortcuts import render, redirect
from django.db.models import Max, Min, Avg, StdDev, Q
from django.db.models.functions import Length
from django.http import HttpResponse
from .models import Alumno, Libro
from .forms import AlumnoForm, InputForm, UpdateAuthorForm
from django.views.generic import TemplateView, View, ListView
import json
from django.core import serializers
from .tasks import send_book, update_b, envio_email

class CreateAlumnoView(View):
    def get(self, request):
        context= {"form": AlumnoForm}
        return render(request, "form.html", context)
    
    def post(self, request):
        form = AlumnoForm(request.POST)

        if form.is_valid():
            Alumno.objects.create(**form.cleaned_data)
            return redirect('index')
        else:
            return redirect('index')

class TemplateIndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["people"] = Alumno.objects.all()
        return context

# class Libros2007(TemplateView):
#     template_name = "index_libros.html"
#     paginate_by = 9

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["libros"] = Libro.objects.filter(publication_date__year__gt='2007')
#         return context

class Libros2007(ListView):
    model = Libro
    paginate_by = 12
    template_name = "index_libros.html"

class Ratings(TemplateView):
    template_name = "index_libros.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ratings"] = Libro.objects.filter(average_rating__range=[3.6, 4.2])
        return context

class FiltroPaginas_y_Rating(TemplateView):
    template_name = "index_libros.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtro"] = Libro.objects.filter(Q(num_pages__gt=400) & Q(average_rating__gt=3.9)).order_by('title')
        return context

class Pags_e_Isbn(TemplateView):
    template_name = "index_libros.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ordenados"] = Libro.objects.order_by('-num_pages','-isbn')
        return context

class Editorial(TemplateView):
    template_name = "index_libros.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editoras"] = Libro.objects.filter(Q(publisher__contains="Books") | Q(publisher__contains="Audio"))
        return context

class FiltrosRating_Pub_y_Reseñas(TemplateView):
    template_name = "index_libros.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtros_varios"] = Libro.objects.filter(average_rating__lt=3.5).exclude(publisher__in=['Vintage', 'Cambridge University Press']).order_by('-text_reviews_count')
        return context

class Meses(TemplateView):
    template_name = "index_libros.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meses"] = Libro.objects.filter(publication_date__month__range=[5,8]).order_by('-average_rating')
        return context

class TotalLibros2007(TemplateView):
    template_name = "total_libros.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        anio_limite = Libro.objects.aggregate(Max('publication_date__year'))

        obj = {}
        for i in range(2008, anio_limite['publication_date__year__max']+1):
            obj[i]=Libro.objects.filter(publication_date__year=i).count()
            
        context["libros"] = obj
        return context

class TitulosTop20(TemplateView):
    template_name = "titulostop.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["libros"] = Libro.objects.annotate(text_len=Length('title')).order_by(-Length('title'))[0:20]
        context["min"] = Libro.objects.annotate(text_len=Length('title')).order_by(-Length('title'))[0:20].aggregate(Min('average_rating'))
        context["max"] = Libro.objects.annotate(text_len=Length('title')).order_by(-Length('title'))[0:20].aggregate(Max('average_rating'))
        context["avg"] = Libro.objects.annotate(text_len=Length('title')).order_by(-Length('title'))[0:20].aggregate(Avg('average_rating'))
        context["desv_stand"] = Libro.objects.annotate(text_len=Length('title')).order_by(-Length('title'))[0:20].aggregate(StdDev('average_rating'))
        return context

class Taller(View):

    # def get_context_data(self, request, **kwargs):
    #     context = super().get_context_data(**kwargs)
        
    def get(self, request):
        template_name = "taller.html"
        object_list = []

        if request.session.get("object_list") is not None:
            object_session = json.loads(request.session.get("object_list"))
            for object in object_session:
                object_list.append(object["fields"])
        else:
            object_list = Libro.objects.all()
            request.session["object_list"] = serializers.serialize('json', object_list)
        # context["object_list"] = Libro.objects.annotate(text_len=Length('publisher')).filter(Q(text_len__lte=20) & Q(text_reviews_count__gt=10))
        # context["object_list"] = Libro.objects.all()
        context = {"object_list": object_list}
        print(context)
        return render(request, template_name, context)

def select_book(request, id):
    book = Libro.objects.get(id=id)
    request.session["authors"] = book.authors
    request.session["id"] = id
    context = {
        "book": book,
        "form": InputForm()
    }

    tema = f"""
- ID: {book.id}
- Título: {book.title}
- Autor(es): {book.authors}
- Rating: {book.average_rating}
- ISBN: {book.isbn}
"""

    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            # send_book.delay(form.cleaned_data["nombre"], form.cleaned_data["email"])
            envio_email.delay(form.cleaned_data["asunto"],"Saludos, soy "+form.cleaned_data["nombre"]+", y aquí te muestro el libro seleccionado:\n"+ tema, form.cleaned_data["email"])
            return HttpResponse("<h2>"+"Nombre: "+form.cleaned_data["nombre"] + " " + "Email: "+form.cleaned_data["email"]+"</h2>")
    return render(request, "oneBook.html", context)

def update_book(request, id):
    book = Libro.objects.filter(id=id)
    request.session["authors"] = book[0].authors
    request.session["id"] = id
    context = {
        "book": book[0],
        "form": UpdateAuthorForm()
    }


    if request.method == "POST":
        form = UpdateAuthorForm(request.POST)
        if form.is_valid():
            update_b.delay(request.session["id"], form.cleaned_data["autor"])
            return redirect('updt',request.session["id"])
            # print(form.cleaned_data["autor"])
            # book.update(authors=form.cleaned_data["autor"])
            # return HttpResponse("<h1>"+"Autor(es): "+form.cleaned_data["autor"]+" (Modificado)"+"</h1>")
            # return render(request, "updatelibro.html", context)
    return render(request, "updatelibro.html", context)

# class CreateAlumnoView(FormView):
#     model = Alumno
#     form_class = AlumnoForm
#     template_name = "form.html"

#     # para guardar la informacion existe lo que es una funcion llamada
#     def form_valid(self, form):
#         Alumno.objects.create(**form.cleaned_data)
#         return redirect('index')

#     def form_invalid(self, form):
#         print("errors", form.errors)
#         return redirect('index')

# class TemplateIndexView(CreateView):
#     template_name = "index.html"
#     model = Alumno
#     fields = ["first_name", "last_name", "idSalon", "nota_laboratorio", "examen"]
#     extra_context = {"people": Alumno.objects.all()}

#siempre las funciones reciben un request
# def index(request):
#     return HttpResponse("<h1>Hello world from django</h1>")

# def index(request):
#     people = Alumno.objects.all()
#     # creando un diccionario
#     context = { 
#         "people": people
#     }

#     # context es una palabra reservada 
#     # si usamos context al momento de pasar nuestro diccionario de datos
#     # unicamente hay que usar el lo keys
#     return render(request, "index.html", context)