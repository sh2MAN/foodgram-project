from django.forms import ModelForm

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'tag', 'cooking_time', 'description', 'image']
        labels = {
            'title': 'Название рецепта',
            'tag': 'Теги',
            'cooking_time': 'Время приготовления',
            'description': 'Описание',
            'image': 'Загрузить фото'
        }
        help_texts = {
            'group': 'Можно указать группу для новой публикации',
            'text': 'Данное поле обязательно для заполнения'
        }
