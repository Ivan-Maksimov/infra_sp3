# Generated by Django 2.2.16 on 2022-08-02 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20220803_0003'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('title',)},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'verbose_name': 'Art work', 'verbose_name_plural': 'Art works'},
        ),
    ]
