from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search_entry, name="search"),
    path("add", views.add_entry, name="add"),
    path("edit/<str:title>", views.edit_entry, name="edit"),
    path("random", views.random, name="random"),
    path("delete/<str:title>", views.delete_entry, name="delete")
]
