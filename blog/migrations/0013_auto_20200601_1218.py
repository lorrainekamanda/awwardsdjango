# Generated by Django 3.0.6 on 2020-06-01 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20200601_0350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='comments',
            field=models.TextField(max_length=1160, null=True),
        ),
    ]
