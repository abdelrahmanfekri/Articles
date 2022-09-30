# Generated by Django 4.1.1 on 2022-09-30 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Social', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='noDislike',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='noLike',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='userDisLike',
            field=models.ManyToManyField(related_name='User_dislike_article', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='userLike',
            field=models.ManyToManyField(related_name='Users_like_article', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='Owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Action',
        ),
    ]
