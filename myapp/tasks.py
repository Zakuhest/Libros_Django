import time
from celery import shared_task
from django.core.mail import send_mail
from .models import Libro
from mysite import settings

@shared_task
def send_book(nombre, mail):
    time.sleep(20)  # Simula operaciones muy pesadas que congelan a Django
    print(nombre + " " + mail)

@shared_task
def update_b(id, autor):
    time.sleep(5)  # Simula operaciones muy pesadas que congelan a Django
    book = Libro.objects.filter(id=id)
    book.update(authors=autor)
    print("Autor(es): " + autor +" (Modificado)")

@shared_task
def envio_email(asunto, tema, email):
    send_mail(
    asunto,
    tema,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently = False
    )
    print("Se envio el correo correctamente")