from django.contrib import admin

from .models import Ingredient, Recipe


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ('title', 'author')
    list_filter = ('author', 'title', 'tags')


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('title', 'units')
    list_filter = ('title',)
