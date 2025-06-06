# Generated by Django 5.2 on 2025-05-05 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_options_alter_product_sort_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, help_text='Manual sort order for product(used in drag-and-drop)'),
        ),
    ]
