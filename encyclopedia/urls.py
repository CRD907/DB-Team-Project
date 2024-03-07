from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create_new", views.newpage, name="newpage"),
    path("search", views.search, name="search"),
    path("get_random/", views.get_random, name="get_random"),
    path("edit_page/<str:title>", views.edit_page, name="edit_page"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("welcome/<str:username>", views.welcome, name="welcome"),
    path('admin/', views.admin_index, name='admin_index'),
    path('admin/create/', views.create_data, name='create_data'),
    path('admin/edit/<int:id>/', views.edit_data, name='edit_data'),
    path('admin/delete/<int:id>/', views.delete_data, name='delete_data'),
    #path("save_page/", views.save_page, name="save_page")
]
