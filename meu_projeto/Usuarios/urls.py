from django.urls import path
from . import views
app_name = 'Usuarios'

urlpatterns = [
    path('registro/', views.Registro, name='registro'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('add-product/', views.add_product, name='add_product'),
    path('remove-product/', views.remove_product, name='remove_product'),
]
    