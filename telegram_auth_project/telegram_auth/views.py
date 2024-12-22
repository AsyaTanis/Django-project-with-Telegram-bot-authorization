import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import TelegramUser
from .models import Post


TELEGRAM_BOT_TOKEN = '7911886663:AAEd1LmYOBmkCGX1Nz3Gs3HF3Zc2S6PuF4g'
TELEGRAM_BOT_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'


def telegram_login(request):
    # Генерация уникального токена для пользователя
    unique_token = request.user.username  # или другой уникальный идентификатор
    telegram_login_url = f'https://t.me/new_my_test1_bot?start={unique_token}'
    return render(request, 'telegram_auth/login.html', {'telegram_login_url': telegram_login_url})


def telegram_callback(request):
    # Получение токена из запроса
    token = request.GET.get('start')

    # Здесь можно добавить логику для получения информации о пользователе из Telegram
    user_info = requests.get(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates').json()

    # Обработка информации о пользователе и создание/обновление записи в базе данных
    if user_info['ok']:
        chat_id = user_info['result'][0]['message']['chat']['id']
        username = user_info['result'][0]['message']['chat'].get('username', '')

        # Проверяем, существует ли уже пользователь
        telegram_user, created = TelegramUser.objects.get_or_create(telegram_id=chat_id)

        if created:
            # Если пользователь новый, создаем нового пользователя Django
            user = User.objects.create(username=username)
            telegram_user.user = user

        telegram_user.username = username
        telegram_user.save()

        # Логин пользователя в системе Django
        login(request, telegram_user.user)

        return redirect('home')

    return redirect('login')

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'telegram_auth/home.html', context)

