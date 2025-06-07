from django.contrib import admin
from .models import GameMap, Vote

@admin.register(GameMap)
class GameMapAdmin(admin.ModelAdmin):
    list_display = ('name',)  # убрали 'game'
    search_fields = ('name',)  # убрали 'game'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_map', 'is_like', 'created_at')
    list_filter = ('is_like', 'created_at')
    search_fields = ('user__username', 'game_map__name')
