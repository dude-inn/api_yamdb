from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# class User(AbstractUser):
#     pass


class Category(models.Model):
    slug = models.SlugField(
        verbose_name='Slug категории',
        max_length=50,
        unique=True,
    )
    title = models.CharField(
        verbose_name='Название категории',
        max_length=250,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Genre(models.Model):
    slug = models.SlugField(
        verbose_name='Slug жанра',
        max_length=50,
        unique=True,
    )
    title = models.CharField(
        verbose_name='Название жанра',
        max_length=250,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг произведения',
        null=True,
        default=None,
    )
    title = models.CharField(
        verbose_name='Название произведения',
        max_length=200,
    )
    year = models.DateTimeField(
        blank=True,
        verbose_name='Год создания произведения',
        format="%Y",
        validators=[validate_year, ]
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['title']


class Review(models.Model):
    """Модель отзывов на произведение."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.CharField(
        'Текст отзыва',
        max_length=200
    )
    author = models.IntegerField(
        'ID пользователя'
    )
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='reviews',
    #     verbose_name='Автор'
    # )
    score = models.IntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={
            'validators': 'Оценка от 1 до 10!'
        }
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            )
        ]
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария к отзыву."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.CharField(
        'Текст комментария',
        max_length=200
    )
    author = models.IntegerField(
        'ID пользователя'
    )
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='comments',
    #     verbose_name='Автор'
    # )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text