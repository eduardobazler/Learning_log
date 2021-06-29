""" Define URL patters for users """

from django.urls import path, include

from users import views

app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('sair_login/', views.sair_lgin, name='sair_login'),
    path('register/', views.register, name='register'),
]
