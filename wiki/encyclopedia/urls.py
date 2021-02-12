from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.get_title, name="get_title"),
    path("search/", views.get_search, name="search_results"),
    path("NewPage/", views.MakeNewPage, name="NewPage"),
    path("wiki", views.RandomPage, name="RandomPage"),
    path("wiki/<str:title>/EditEntry", views.EditEntry, name="EditEntry"),
    path("wiki/<str:title>/submit", views.submitEdit, name="submitEdit")
]
