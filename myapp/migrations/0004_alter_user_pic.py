# Generated by Django 3.2.9 on 2021-12-03 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_user_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pic',
            field=models.FileField(default='avtar.png', upload_to='Profile'),
        ),
    ]