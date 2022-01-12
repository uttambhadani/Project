# Generated by Django 3.2.9 on 2021-12-24 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('pay_amount', models.IntegerField()),
                ('pay_id', models.CharField(max_length=20)),
                ('order_id', models.CharField(max_length=20)),
                ('address', models.TextField(blank=True, null=True)),
                ('coupon', models.CharField(blank=True, max_length=20, null=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('expected_del', models.DateField()),
                ('status', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.product')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]