# Generated by Django 2.2.16 on 2022-08-01 22:00

import django.core.validators
from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20220802_0052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'Genre', 'verbose_name_plural': 'Genries'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'verbose_name': 'Art work', 'verbose_name_plural': 'Art works'},
        ),
        migrations.RenameField(
            model_name='title',
            old_name='slug',
            new_name='genre',
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(validators=[reviews.validators.validate_year], verbose_name='Year'),
        ),
    ]