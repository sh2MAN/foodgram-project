from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Basket, Ingredient, Recipe, RecipeIngredients
from .utils import get_filter_tags, get_list_ingredients

User = get_user_model()


def index(request):
    tags = request.GET.get('tags')

    if tags:
        recipes = Recipe.objects.filter(
            get_filter_tags(tags)
        ).select_related('author')
    else:
        recipes = Recipe.objects.select_related('author').all()

    paginator = Paginator(recipes, settings.NUM_ELEMENTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page, 'paginator': paginator, 'tags': tags
    }
    return render(request, 'index.html', context)


def recipe_author(request, author):
    author = get_object_or_404(User, username=author)
    tags = request.GET.get('tags')

    if tags:
        recipes = author.recipes.filter(get_filter_tags(tags))
    else:
        recipes = author.recipes.all()

    paginator = Paginator(recipes, settings.NUM_ELEMENTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'author': author,
        'page': page,
        'paginator': paginator,
        'tags': tags
    }
    return render(request, 'authorRecipe.html', context)


def recipe_single_page(request, author, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author__username=author)
    ingredients = recipe.ingredients.all()
    context = {
        'author': recipe.author,
        'recipe': recipe,
        'ingredients': ingredients
    }
    return render(request, 'singlePage.html', context)


@login_required
def add_recipe(request):
    form_title = 'Создание рецепта'
    button_caption = 'Создать рецепт'
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        ingredients = get_list_ingredients(request.POST)

        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()

        for name, value in ingredients.items():
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=get_object_or_404(Ingredient, title=name),
                quantity=value
            )
        form.save_m2m()
        return redirect('index')

    context = {
        'form': form, 'form_title': form_title,
        'button_caption': button_caption
    }

    return render(request, 'formRecipe.html', context)


def favorite(request):
    tags = request.GET.get('tags')
    user = get_object_or_404(User, id=request.user.id)

    if tags:
        recipes = Recipe.objects.filter(
            get_filter_tags(tags)
        ).filter(favorite_user__user=user)
    else:
        recipes = Recipe.objects.filter(favorite_user__user=user)

    paginator = Paginator(recipes, settings.NUM_ELEMENTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, 'tags': tags}
    return render(request, 'favorite.html', context)


@login_required
def my_subscribe(request):
    authors = request.user.subscriber.annotate(
        num_recipe=Count('author__recipes')
    ).all()

    paginator = Paginator(authors, settings.NUM_ELEMENTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator}
    return render(request, 'myFollow.html', context)


@login_required
def edit_recipe(request, author, recipe_id):
    form_title = 'Редактирование рецепта'
    button_caption = 'Сохранить'

    user = get_object_or_404(User, username=author)

    if request.user != user:
        return redirect('recipe', author, recipe_id)

    recipe = get_object_or_404(
        Recipe, pk=recipe_id, author=user
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
                ingredient=get_object_or_404(Ingredient, title=name),
                quantity=value
            )
        form.save_m2m()
        return redirect('recipe', author, recipe_id)

    context = {
        'form': form, 'recipe': recipe, 'is_edit': True,
        'form_title': form_title, 'button_caption': button_caption
    }

    return render(request, 'formRecipe.html', context)


@login_required
def delete_recipe(request, author, recipe_id):
    user = get_object_or_404(User, username=author)
    if request.user == user:
        Recipe.objects.filter(id=recipe_id, author=user).delete()
    return redirect('index')


@login_required
def shopping_list(request):
    recipes = Basket.objects.filter(user=request.user)
    return render(request, 'shopList.html', {'recipes': recipes})
