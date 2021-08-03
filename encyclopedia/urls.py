from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.pages, name="pages"),
    path("redirectPage", views.redirectPage, name="redirectPage"),
    path("wiki/search/<str:name>", views.search, name="search"),
    path("createNewPage", views.createNewPage, name="createNewPage"),
    path("randomPage", views.randomPage, name="randomPage"),
    path("edit/<str:name>", views.edit, name="edit"),
]
