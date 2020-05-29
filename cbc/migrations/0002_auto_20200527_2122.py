# Generated by Django 2.2 on 2020-05-27 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cbc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodsmear',
            name='cbc',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cbc.CompleteBloodCount', verbose_name='Общий анализ крови'),
        ),
        migrations.AlterField(
            model_name='fivediff',
            name='cbc',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cbc.CompleteBloodCount', verbose_name='Общий анализ крови'),
        ),
        migrations.AlterField(
            model_name='threediff',
            name='cbc',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cbc.CompleteBloodCount', verbose_name='Общий анализ крови'),
        ),
    ]
