# Generated by Django 4.1.3 on 2023-03-13 03:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('english_list', '0005_wordlists_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordlists',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to=settings.AUTH_USER_MODEL),
        ),
    ]
