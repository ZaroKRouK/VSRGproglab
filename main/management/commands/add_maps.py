
from django.core.management.base import BaseCommand
from main.models import GameMap

class Command(BaseCommand):
    help = 'Добавляет тестовые карты в базу данных'

    def handle(self, *args, **options):
        maps_data = [
            {
                'name': 'DDR A3',
                'game': 'Dance Dance Revolution',
                'image': 'images/DDRlogo.jpeg'
            },
            {
                'name': 'Sound Voltex VI',
                'game': 'Sound Voltex',
                'image': 'images/SoundVoltexLogo.jpeg'
            },
            {
                'name': 'Etterna',
                'game': 'Etterna',
                'image': 'images/etterna logo.jpeg'
            },
            {
                'name': 'osu!mania',
                'game': 'osu!',
                'image': 'images/o!m logo.jpeg'
            }
        ]

        for map_data in maps_data:
            game_map, created = GameMap.objects.get_or_create(
                name=map_data['name'],
                defaults={
                    'game': map_data['game'],
                    'image': map_data['image'],
                    'likes': 0,
                    'dislikes': 0
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Создана карта: {game_map.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Карта уже существует: {game_map.name}')
                )
