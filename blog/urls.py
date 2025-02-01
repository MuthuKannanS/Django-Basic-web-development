from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path("", views.index, name="index" ),
    path("post/<str:slug>", views.detail, name="detail"),
    path("about", views.about, name="about" ),    
    path("register", views.register, name="register" ),
    path("contact", views.contact, name="contact" ),
    path("login", views.login, name="login" ),
    path("dashboard", views.dashboard, name="dashboard" ),
    path("logout", views.logout, name="logout" ),
    path("forgotpassword", views.forgotpassword, name="forgotpassword" ),
    path("newpost", views.newpost, name="newpost" ),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post" ),
    path("delete_post/<int:post_id>", views.delete_post, name="delete_post" ),
    path("publish_post/<int:post_id>", views.publish_post, name="publish_post" ),
    
  ]