from django.urls import path
from . import views, auth
urlpatterns = [
    path('',views.index),
    path('login', auth.login),
    path('registro', auth.registro),
    path('logout', auth.logout),
    path('wall', views.wall),
    path('post_message', views.post_message),
    path('delete/<int:id>', views.delete_comment),
    path('add_comment/<int:id>', views.post_comment),
    # path('user_profile/<int:id>', views.profile),
]
