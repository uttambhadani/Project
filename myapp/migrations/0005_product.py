# Generated by Django 3.2.9 on 2021-12-03 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_user_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('price', models.CharField(max_length=10)),
                ('quantity', models.IntegerField()),
                ('category', models.CharField(max_length=20)),
                ('pic', models.FileField(blank=True, null=True, upload_to='Products')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]