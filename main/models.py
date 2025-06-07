from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Q

class GameMap(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_user_vote(self, user):
        if not user.is_authenticated:
            return None
        vote = self.votes.filter(user=user).first()
        return vote.is_like if vote else None

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_map = models.ForeignKey(GameMap, on_delete=models.CASCADE, related_name="votes")
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game_map')