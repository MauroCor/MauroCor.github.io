from django.urls import path

from . import views

urlpatterns = [
    path("monthly", views.get_fixed_costs, name="fixed_cost_list"),
    path('set_fixed_cost', views.set_fixed_cost, name='set_fixed_cost'),
]
