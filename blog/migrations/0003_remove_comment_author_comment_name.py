# Generated by Django 5.1.3 on 2024-11-22 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(default='User', max_length=250),
        ),
    ]
