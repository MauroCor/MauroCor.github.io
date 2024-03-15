from django.urls import path

from . import views

urlpatterns = [
    path("lista_gastos", views.lista_gastos, name="lista_gastos"),
    path("agregar_gasto", views.agregar_gasto, name="agregar_gasto"),
    path("lista_ingresos", views.lista_ingresos, name="lista_ingresos"),
    path("agregar_ingreso", views.agregar_ingreso, name="agregar_ingreso"),
]
