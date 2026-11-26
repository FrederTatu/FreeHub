from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("freelancers/", views.freelancers, name="freelancers"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("project/<int:project_id>/", views.project, name="project"),
    path("add-project/", views.add_project, name="add_project"),
    path("account/", views.account, name="account"),
    path("register/", views.register, name="register"),
    
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("project/<int:project_id>/edit/", views.edit_project, name="edit_project"),
    path("project/<int:project_id>/delete/", views.delete_project, name="delete_project"),
]