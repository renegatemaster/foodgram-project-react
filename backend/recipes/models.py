from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Ingredient(models.Model):
    '''Ingredient model.'''
    name = models.CharField(
        _('название ингредиента'),
        max_length=200,
        db_index=True
    )
    measurement_unit = models.CharField(_('единица измерения'), max_length=50)

    class Meta:
        verbose_name = _('ингредиент')
        verbose_name_plural = _('ингредиенты')
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class Tag(models.Model):
    '''Tag model.'''
    name = models.CharField(_('имя тега'), max_length=200, unique=True)
    color = models.CharField(_('HEX-цвет тега'), max_length=7, unique=True)
    slug = models.SlugField(_('слаг тега'), max_length=200, unique=True)

    class Meta:
        verbose_name = _('тег')
        verbose_name_plural = _('теги')

    def __str__(self):
        return f'{self.Meta.verbose_name} "{self.name}".'


class Recipe(models.Model):
    '''Recipe model.'''
    author = models.ForeignKey(
        User,
        related_name='recipes',
        verbose_name=_('автор'),
        on_delete=models.SET_NULL,
        null=True
    )
    name = models.CharField(
        _('название рецепта'),
        max_length=200,
        db_index=True,
        help_text=_('Обязательное. 200 символов или менее.')
    )
    image = models.ImageField(
        _('картинка блюда'),
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    text = models.TextField(_('описание'), help_text=_('Обязательное.'))
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='IngredientInRecipe',
        verbose_name=_('ингредиенты')
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name=_('теги')
    )
    cooking_time = models.PositiveSmallIntegerField(
        _('время приготовления'),
        help_text=_('Обязательное. 1 минута или более.'),
        validators=[
            MinValueValidator(
                limit_value=1,
                message=_('Минимальное время приготовления — 1 минута.')
            )
        ]
    )

    class Meta:
        verbose_name = _('рецепт')
        verbose_name_plural = _('рецепты')
        ordering = ['-id']

    def __str__(self):
        return f'{self.Meta.verbose_name} "{self.name}".'


class IngredientInRecipe(models.Model):
    '''Model for ingredients in recipe.'''
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name=_('ингредиенты'),
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredient_list',
        verbose_name=_('рецепт'),
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        _('количество'),
        validators=[
            MinValueValidator(
                limit_value=1,
                message=_('Минимальное количество — 1.')
            )
        ]
    )

    class Meta:
        verbose_name = _('ингредиент в рецепте')
        verbose_name_plural = _('ингредиенты в рецепте')

    def __str__(self):
        return f'{self.recipe}: "{self.ingredient}" — {self.quantity}'


class Favorite(models.Model):
    '''Model for adding to favorite.'''
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name=_('пользователь')
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name=_('рецепт')
    )

    class Meta:
        verbose_name = _('избранное')
        verbose_name_plural = _('избранные')

    def __str__(self):
        return f'{self.Meta.verbose_name} {self.user.__str__()}.'


class ShoppingCart(models.Model):
    '''Model for adding to cart.'''
    user = models.ForeignKey(
        User,
        related_name='cart',
        on_delete=models.CASCADE,
        verbose_name=_('пользователь')
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='cart',
        on_delete=models.CASCADE,
        verbose_name=_('рецепт')
    )

    class Meta:
        verbose_name = _('корзина')
        verbose_name_plural = _('корзины')

    def __str__(self):
        return f'{self.Meta.verbose_name} {self.user.__str__()}.'
