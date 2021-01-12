from django.contrib.auth import get_user_model
from django.db import models
from multiselectfield import MultiSelectField

User = get_user_model()


class Ingredient(models.Model):
    """Ингридиенты"""
    title = models.CharField('Ингредиент', max_length=100)
    dimension = models.CharField('Мера веса', max_length=25)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.title} {self.dimension}'


class Recipe(models.Model):
    """Рецепты"""
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'
    TAGS_CHOICES = [
        (BREAKFAST, 'Завтрак'),
        (LUNCH, 'Обед'),
        (DINNER, 'Ужин')
    ]
    TAGS_COLORS = {
        BREAKFAST: 'orange',
        LUNCH: 'green',
        DINNER: 'purple'
    }
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField('Название рецепта', max_length=100)
    image = models.ImageField('Изображение', upload_to='recipes/')
    description = models.TextField('Описание')
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        verbose_name='Ингредиенты'
    )
    tags = MultiSelectField(
        'Теги',
        choices=TAGS_CHOICES,
        max_choices=3,
        null=True
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления'
    )
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
    """Связующая таблица между рецептом и ингридиентами"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Количество')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredients'
            )
        ]
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиент в рецепте(ах)'


class Basket(models.Model):
    """Список покупок"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='basket_recipes'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='basket_users'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipes_basket'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
