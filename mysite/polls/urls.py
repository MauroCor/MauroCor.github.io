from django.urls import path

from . import views

urlpatterns = [
    path("monthly", views.gets, name="gets"),
    path('set_fixed_cost', views.set_fixed_cost, name='set_fixed_cost'),
    path('set_earning', views.set_earning, name='set_earning'),
]
