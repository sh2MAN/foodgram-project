from django.forms import ModelForm

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'tags', 'cooking_time', 'description', 'image']
        labels = {
            'title': 'Название рецепта',
            'tags': 'Теги',
            'cooking_time': 'Время приготовления',
            'description': 'Описание',
            'image': 'Загрузить фото'
        }
        help_texts = {
            'title': 'Укажите название рецепта',
            'description': 'Опишите рецепт или способ приготовления'
        }
