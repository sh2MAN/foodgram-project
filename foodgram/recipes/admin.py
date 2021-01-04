from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredients, Basket


class IngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ('title', 'author')
    list_filter = ('author', 'title', 'tags')
    ordering = ('-pub_date',)
    inlines = (IngredientsInline,)


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('title', 'dimension')
    list_filter = ('title',)


class RecipeIngredientsAdmin(admin.ModelAdmin):
    model = RecipeIngredients
    list_display = ('recipe', 'ingredient')


class BasketAdmin(admin.ModelAdmin):
    model = Basket
    list_display = ('user', 'recipe')
    list_filter = ('user',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientsAdmin)
admin.site.register(Basket, BasketAdmin)
