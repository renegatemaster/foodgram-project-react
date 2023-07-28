# Generated by Django 3.2.3 on 2023-07-28 06:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20230727_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(help_text='Обязательное. 1 минута или более.', validators=[django.core.validators.MinValueValidator(limit_value=1, message='Минимальное время приготовления — 1 минута.')], verbose_name='время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(db_index=True, help_text='Обязательное. 200 символов или менее.', max_length=200, verbose_name='название рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(help_text='Обязательное.', verbose_name='описание'),
        ),
    ]
