# Generated by Django 5.0.6 on 2024-05-29 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_balance_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
