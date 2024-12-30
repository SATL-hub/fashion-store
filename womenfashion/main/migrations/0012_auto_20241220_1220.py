# Generated by Django 3.2.25 on 2024-12-20 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_orderitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='payment_mode',
            field=models.CharField(choices=[('Pay_On_Delivery', 'Pay_On_Delivery'), ('Online_Payment', 'Online_Payment')], max_length=100),
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('message', models.TextField()),
                ('rating', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.userprofile')),
            ],
        ),
    ]