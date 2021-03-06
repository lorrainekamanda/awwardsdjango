# Generated by Django 3.0.6 on 2020-06-01 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0017_auto_20200601_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='likes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comments',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Profile'),
        ),
        migrations.AddField(
            model_name='comments',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comments',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Image'),
        ),
    ]
