from django.urls import path
from . import views

urlpatterns = [
    path('update_comment', views.update_comment, name='update_comment'),
    path('reply_is_login', views.reply_is_login, name='reply_is_login'),
]
