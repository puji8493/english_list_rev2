from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """カスタムユーザーモデル"""

    class Meta(AbstractUser.Meta):
        db_table = 'custom_user'
