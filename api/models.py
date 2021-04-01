from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .validators import validate_year


class Category(models.Model):
    # Можно лучше: Всем полям и моделям добавляем verbose name
    name = models.CharField(
        verbose_name='Наименование',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='URL slug',
        unique=True
    )

    # Надо исправить:
    # Согласно кодстайлу джанго, в моделях сначала должен идти class Meta,
    # а потом __str__. Напоминаю об этом
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='URL slug',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=200
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год',
        validators=[validate_year],
        # Можно лучше: рассказываем про индексы
        db_index=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        through_fields=('title', 'genre'),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-id']


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )


# Надо исправить: Роли описаны в виде чойсов.
# Лучше так, чем просто списком кортежей, ниже объясню почему
class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(
        max_length=99,
        blank=True,
        editable=False,
        null=True,
        unique=True
    )
    role = models.CharField(
        # Можно лучше: Тут обычно задают 9, как в moderator.
        # Я бы закладывался сразу с запасом
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER
    )
    bio = models.TextField(blank=True)

    # Можно лучше: можно добавить тут property для удобства
    @property
    def is_admin(self):
        # Надо исправить: Везде, где мы используем роли - не используем строки,
        # а используем константу
        return (
                self.role == UserRole.ADMIN or
                self.is_superuser or
                # Я тут не уверен, считается ли стафф "администратором Django"
                # по спеке, но будем считать, что да
                self.is_staff)

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    # Надо исправить: Здесь используем IntegerField (часто вижу Float) +
    # обязательно добавляем валидацию
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1'),
            MaxValueValidator(10, 'Оценка не может быть выше 10')
        ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        # Можно лучше: Не забываем добавлять сортировку.
        # Можно, конечно, в кверисете вьюсета, но лучше здесб
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.title}, {self.score}, {self.author}'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.author}, {self.pub_date}: {self.text}'
