from django.urls import path
from .views import telegram_login, telegram_callback, home

urlpatterns = [
    path('login/', telegram_login, name='login'),
    path('callback/', telegram_callback, name='callback'),
    path('', home, name="home_page")
]
