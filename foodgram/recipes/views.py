from functools import reduce

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .helpers import get_list_ingredients
from .models import Basket, Ingredient, Recipe, RecipeIngredients

User = get_user_model()


def index(request):
    tags = request.GET.get('tags', None)
    if tags:
        recipe_list = Recipe.objects.filter(
            reduce(
                lambda x, y: x | y, [Q(tags__contains=tag)
                                     for tag in tags.split('|')]
            )
        ).select_related('author').all()
    else:
        recipe_list = Recipe.objects.select_related('author').all()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'index.html', {'page': page,
                                'paginator': paginator, 'tags': tags}
    )


def recipe_author(request, author):
    author = get_object_or_404(User, username=author)
    tags = request.GET.get('tags', None)
    if tags:
        recipe_list = author.user_recipes.filter(
            reduce(
                lambda x, y: x | y, [Q(tags__contains=tag)
                                     for tag in tags.split('|')]
            )
        ).all()
    else:
        recipe_list = author.user_recipes.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'author': author,
        'page': page,
        'paginator': paginator,
        'tags': tags
    }
    return render(
        request,
        'authorRecipe.html',
        context=context
    )


def recipe_single_page(request, author, recipe_id):
    author = get_object_or_404(User, username=author)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=author)
    ingredients = recipe.ingredients.all()
    return render(
        request,
        'recipe_single_page.html',
        {'author': author, 'recipe': recipe, 'ingredients': ingredients}
    )


@login_required
def add_recipe(request):
    form_title = 'Создание рецепта'
    button_caption = 'Создать рецепт'
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if request.method == "POST" and form.is_valid():
        ingredients = get_list_ingredients(request.POST)

        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()

        for name, value in ingredients.items():
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(title=name),
                quantity=value
            )
        form.save_m2m()
        return redirect('index')

    context = {
        'form': form, 'form_title': form_title,
        'button_caption': button_caption
    }

    return render(request, 'formRecipe.html', context=context)


def favorite(request):
    tags = request.GET.get('tags', None)
    if tags:
        recipes = request.user.favorites.filter(
            reduce(
                lambda x, y: x | y, [Q(recipe__tags__contains=tag)
                                     for tag in tags.split('|')]
            )
        ).all()
    else:
        recipes = request.user.favorites.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, 'tags': tags}
    return render(request, 'favorite.html', context=context)


@login_required
def my_subscribe(request):
    authors = request.user.subscriber.annotate(
        num_recipe=Count('author__user_recipes')
    ).all()
    print(authors)
    paginator = Paginator(authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator}
    return render(request, 'myFollow.html', context=context)


@login_required
def edit_recipe(request, author, recipe_id):
    form_title = 'Редактирование рецепта'
    button_caption = 'Сохранить'

    if request.user.username != author:
        return redirect('recipe', author, recipe_id)

    recipe = get_object_or_404(
        Recipe, pk=recipe_id, author__username=author
    )
    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )

    ingredients = get_list_ingredients(request.POST)
    if form.is_valid():
        RecipeIngredients.objects.filter(recipe=recipe).delete()

        recipe = form.save(commit=False)
        recipe.save()

        for name, value in ingredients.items():
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(title=name),
                quantity=value
            )
        form.save_m2m()
        return redirect('recipe', author, recipe_id)

    context = {
        'form': form, 'recipe': recipe, 'is_edit': True,
        'form_title': form_title, 'button_caption': button_caption
    }

    return render(request, 'formRecipe.html', context=context)


@login_required
def delete_recipe(request, author, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.username == author:
        recipe.delete()
    return redirect('index')


def shopping_list(request):
    recipes = Basket.objects.filter(user=request.user).all()
    return render(request, 'shopList.html', {'recipes': recipes})
