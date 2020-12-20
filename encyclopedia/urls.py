from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.title, name="title"),
    path("searchresult", views.searchresult, name="search"),
    path("create", views.create, name="create"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("random", views.randompage, name="random")
]
