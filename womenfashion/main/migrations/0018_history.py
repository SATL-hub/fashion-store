# Generated by Django 3.2.25 on 2024-12-26 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_profilepic_resume'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=100)),
                ('no_of_item', models.IntegerField()),
                ('size', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('individual_price', models.CharField(max_length=100)),
                ('total_price', models.CharField(max_length=100)),
                ('payment_mode', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Out for shipping', 'Out for shipping'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='pending', max_length=150)),
                ('ordered_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.userprofile')),
            ],
        ),
    ]
