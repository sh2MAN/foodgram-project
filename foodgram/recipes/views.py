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
    tags = request.GET.get('tags', None)

    if tags:
        recipe_list = Recipe.objects.filter(
            get_filter_tags(tags)
        ).select_related('author').all()
    else:
        recipe_list = Recipe.objects.select_related('author').all()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page, 'paginator': paginator, 'tags': tags
    }
    return render(request, 'index.html', context)


def recipe_author(request, author):
    author = get_object_or_404(User, username=author)
    tags = request.GET.get('tags', None)

    if tags:
        recipe_list = author.user_recipes.filter(
            get_filter_tags(tags)
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
    return render(request, 'authorRecipe.html', context)


def recipe_single_page(request, author, recipe_id):
    author = get_object_or_404(User, username=author)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=author)
    ingredients = recipe.ingredients.all()
    context = {'author': author, 'recipe': recipe, 'ingredients': ingredients}
    return render(request, 'singlePage.html', context)


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

    return render(request, 'formRecipe.html', context)


def favorite(request):
    tags = request.GET.get('tags', None)
    user = get_object_or_404(User, username=request.user.username)

    if tags:
        recipes = Recipe.objects.filter(
            get_filter_tags(tags)
        ).filter(favorite_user__user=user).all()
    else:
        recipes = Recipe.objects.filter(favorite_user__user=user).all()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, 'tags': tags}
    return render(request, 'favorite.html', context)


@login_required
def my_subscribe(request):
    authors = request.user.subscriber.annotate(
        num_recipe=Count('author__user_recipes')
    ).all()

    paginator = Paginator(authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator}
    return render(request, 'myFollow.html', context)


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

    return render(request, 'formRecipe.html', context)


@login_required
def delete_recipe(request, author, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.username == author:
        recipe.delete()
    return redirect('index')


@login_required
def shopping_list(request):
    recipes = Basket.objects.filter(user=request.user).all()
    return render(request, 'shopList.html', {'recipes': recipes})
