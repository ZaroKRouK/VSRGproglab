from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import GameMap, Vote

def home(request):
    return render(request, 'mainpage.html')

def library(request):
    return render(request, 'library.html')

def history(request):
    return render(request, 'history.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('library')
        else:
            messages.error(request, 'Неверные данные для входа')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, 'Регистрация прошла успешно!')
        return redirect('library')

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')

def vote_api(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Необходимо войти в систему'})

        try:
            data = json.loads(request.body)
            map_id = data.get('map_id')
            is_like = data.get('is_like')

            game_map = GameMap.objects.get(id=map_id)

            existing_vote = Vote.objects.filter(user=request.user, game_map=game_map).first()

            if existing_vote:
                if existing_vote.is_like == is_like:
                    existing_vote.delete()
                    user_vote = None
                else:
                    existing_vote.is_like = is_like
                    existing_vote.save()
                    user_vote = is_like
            else:
                Vote.objects.create(user=request.user, game_map=game_map, is_like=is_like)
                user_vote = is_like

            likes_count = Vote.objects.filter(game_map=game_map, is_like=True).count()
            dislikes_count = Vote.objects.filter(game_map=game_map, is_like=False).count()

            game_map.likes = likes_count
            game_map.dislikes = dislikes_count
            game_map.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'votes',
                {
                    'type': 'vote_update',
                    'message': {
                        'map_id': map_id,
                        'likes': likes_count,
                        'dislikes': dislikes_count,
                    }
                }
            )

            return JsonResponse({
                'success': True,
                'likes': likes_count,
                'dislikes': dislikes_count,
                'user_vote': user_vote
            })

        except GameMap.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Карта не найдена'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Метод не разрешен'})


def stats_api(request):
    maps = GameMap.objects.all()
    stats = []

    for game_map in maps:
        user_vote = None
        if request.user.is_authenticated:
            try:
                vote = Vote.objects.get(user=request.user, game_map=game_map)
                user_vote = vote.is_like
            except Vote.DoesNotExist:
                pass

        stats.append({
            'id': game_map.id,
            'likes': game_map.likes,
            'dislikes': game_map.dislikes,
            'user_vote': user_vote
        })

    return JsonResponse({'maps': stats})
