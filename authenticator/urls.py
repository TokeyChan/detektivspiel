from django.urls import path

from . import views

app_name = 'auth'
urlpatterns = [
    path('login/', views.log_in, name='login'),
    path('check/', views.check, name='check'),
    path('logout/', views.log_out)
]
