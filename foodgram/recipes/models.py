from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

User = get_user_model()


TAGS = (
    ('breakfast', _('Breakfast')),
    ('lunch', _('Lunch')),
    ('dinner', _('Dinner'))
)


class Ingredient(models.Model):
    """Ингридиенты"""
    title = models.CharField(_('Ingredient'), max_length=50)
    units = models.CharField(_('Unit of measure'), max_length=10)

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')


class Recipe(models.Model):
    """Рецепты"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_recipes'
    )
    title = models.CharField(_('Title'), max_length=50)
    image = models.ImageField(_('Image of the dish'))
    description = models.TextField(_('Description'))
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        verbose_name=_('Ingredients')
    )
    tag = MultiSelectField(
        _('Tags'),
        choices=TAGS,
        max_choices=3,
        max_length=3
    )
    cooking_time = models.SmallIntegerField(
        _('Cooking time')
    )
    slug = slugify(title)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')


class RecipeIngredients(models.Model):
    """Связующая таблица между рецептом и ингридиентами для него"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(_('Quantity'))

    class Meta:
        verbose_name = _('Ingredient for the recipe')
        verbose_name_plural = _('Ingredients for the recipe')
