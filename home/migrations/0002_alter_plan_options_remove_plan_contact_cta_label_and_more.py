# Generated by Django 5.2 on 2025-04-21 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plan',
            options={},
        ),
        migrations.RemoveField(
            model_name='plan',
            name='contact_cta_label',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='cta_label',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='icon_class',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='order',
        ),
    ]
