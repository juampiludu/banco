from django.urls import path
from . import views

urlpatterns = [
    
    path('informe/', views.informe, name='informe'),

]
