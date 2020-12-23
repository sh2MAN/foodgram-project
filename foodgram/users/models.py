from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ungettext_lazy as _
from recipes.models import Recipe

User = get_user_model()


class Subscription(models.Model):
    """Подписики на авторов"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscriptions'
            )
        ]
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')


class Favorite(models.Model):
    """Избранные рецепты пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_user'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorites'
            )
        ]
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')
