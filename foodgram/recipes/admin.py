from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredients


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ('title', 'author')
    list_filter = ('author', 'title', 'tags')
    ordering = ('-pub_date',)


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('title', 'units')
    list_filter = ('title',)


class RecipeIngredientsAdmin(admin.ModelAdmin):
    model = RecipeIngredients
    list_display = ('recipe__title', 'ingredient__title')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientsAdmin)
