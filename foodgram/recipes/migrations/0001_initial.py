# Generated by Django 2.2 on 2021-01-08 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Ингредиент')),
                ('dimension', models.CharField(
                    max_length=25, verbose_name='Мера веса')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(
                    max_length=100, verbose_name='Название рецепта')),
                ('image', models.ImageField(
                    upload_to='recipes/', verbose_name='Изображение')),
                ('description', models.TextField(verbose_name='Описание')),
                ('tags', multiselectfield.db.fields.MultiSelectField(choices=[('breakfast', 'Завтрак'), (
                    'lunch', 'Обед'), ('dinner', 'Ужин')], max_length=22, null=True, verbose_name='Теги')),
                ('cooking_time', models.PositiveSmallIntegerField(
                    verbose_name='Время приготовления')),
                ('pub_date', models.DateTimeField(
                    auto_now=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name='user_recipes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredients',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(
                    verbose_name='Количество')),
                ('ingredient', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='recipes.Ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name='ingredients', to='recipes.Recipe')),
            ],
            options={
                'verbose_name': 'Ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиент в рецепте(ах)',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(
                through='recipes.RecipeIngredients', to='recipes.Ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name='basket_users', to='recipes.Recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                           related_name='basket_recipes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Список покупок',
            },
        ),
        migrations.AddConstraint(
            model_name='recipeingredients',
            constraint=models.UniqueConstraint(
                fields=('recipe', 'ingredient'), name='unique_ingredients'),
        ),
        migrations.AddConstraint(
            model_name='basket',
            constraint=models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_recipes_basket'),
        ),
    ]
