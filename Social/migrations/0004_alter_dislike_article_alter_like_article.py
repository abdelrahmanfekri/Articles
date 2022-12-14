# Generated by Django 4.1.1 on 2022-09-30 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Social', '0003_like_dislike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dislike',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dislike_article', to='Social.article'),
        ),
        migrations.AlterField(
            model_name='like',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_article', to='Social.article'),
        ),
    ]
