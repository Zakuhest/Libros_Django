from django import forms
from .models import Salon

class AlumnoForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    idSalon = forms.ModelChoiceField(queryset=Salon.objects.all(), empty_label=None)
    nota_laboratorio = forms.FloatField(min_value=0.0)
    examen = forms.FloatField(min_value=0.0)

class InputForm(forms.Form):
    nombre = forms.CharField(max_length=200)
    email = forms.EmailField()
    asunto = forms.CharField(max_length=200)
    #tema = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))

class UpdateAuthorForm(forms.Form):
    autor = forms.CharField(max_length=250)