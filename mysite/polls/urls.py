from django.urls import path

from . import views

urlpatterns = [
    path("fixed_cost_list", views.fixed_cost_list, name="fixed_cost_list"),
]
