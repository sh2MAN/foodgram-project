from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from multiselectfield import MultiSelectField

User = get_user_model()


TAGS = (
    ('breakfast', 'Завтрак'),
    ('lunch', 'Обед'),
    ('dinner', 'Ужин')
)


class Ingredient(models.Model):
    """Ингридиенты"""
    title = models.CharField('Ингредиент', max_length=50)
    units = models.CharField('Мера веса', max_length=10)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.title} {self.units}'


class Recipe(models.Model):
    """Рецепты"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_recipes'
    )
    title = models.CharField('Название', max_length=50)
    image = models.ImageField('Изображение', upload_to="recipes/")
    description = models.TextField('Описание')
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        verbose_name='Ингредиенты'
    )
    tag = MultiSelectField(
        'Тег',
        choices=TAGS,
        max_choices=3
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления'
    )
    slug = slugify(title)
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.title} от пользователя {self.author.username}'


class RecipeIngredients(models.Model):
    """Связующая таблица между рецептом и ингридиентами для него"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Количество')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_favorites'
            )
        ]
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиент в рецепте(ах)'
