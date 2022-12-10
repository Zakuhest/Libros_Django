from django.urls import path
from . import views

urlpatterns=[
    # path('', views.index, name='index')
    path('', views.TemplateIndexView.as_view(), name='index'),
    path('crear/', views.CreateAlumnoView.as_view(), name='crear'),
    path('libros/1q', views.Libros2007.as_view(), name='libros1'),
    path('libros/2q', views.TotalLibros2007.as_view(), name='libros2'),
    path('libros/3q', views.Ratings.as_view(), name='libros3'),
    path('libros/4qy5q', views.TitulosTop20.as_view(), name='libros4'),
    path('libros/6q', views.FiltroPaginas_y_Rating.as_view(), name='libros5'),
    path('libros/7q', views.Pags_e_Isbn.as_view(), name='libros6'),
    path('libros/8q', views.Editorial.as_view(), name='libros7'),
    path('libros/9q', views.FiltrosRating_Pub_y_Reseñas.as_view(), name='libros8'),
    path('libros/10q', views.Meses.as_view(), name='libros9'),
    path('libros/11q', views.Taller.as_view(), name='libros10'),
    path('libros/<int:id>', views.select_book, name='select'),
    path('libros/update/<int:id>', views.update_book, name='updt'),
]