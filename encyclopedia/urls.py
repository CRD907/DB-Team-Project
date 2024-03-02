from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create_new", views.newpage, name="newpage"),
    path("search", views.search, name="search"),
    path("get_random/", views.get_random, name="get_random"),
    path("edit_page/<str:title>", views.edit_page, name="edit_page"),
    #path("save_page/", views.save_page, name="save_page")
]
