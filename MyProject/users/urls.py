from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin_page, name='dashboard_admin'),
    path('cliente/', client_page, name='dashboard_client'),
]