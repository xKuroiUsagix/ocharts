from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='osu_profile'
    )
    osu_id = models.IntegerField(unique=True)
    osu_avatar = models.URLField(max_length=512)
    osu_username = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
