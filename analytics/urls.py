from django.urls import path
from . import views

urlpatterns = [
    path("latest", views.index,name="latest"),
    path("search/<str:mode>",views.search ,name="search"),
    path("csv/",views.csv,name="csv"),
    path("weekly/",views.weekly,name="weekly"),
    path("monthly/",views.monthly,name="monthly"),
    path("",views.dummy,name="dummy"),
]
