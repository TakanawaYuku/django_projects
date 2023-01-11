from django.db import models
from django.shortcuts import reverse
import uuid  # Требуется для уникальных экземпляров книги
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Genre(models.Model):
    """
        Модель, представляющая книжный жанр (например, научная фантастика, документальная литература).
    """
    name = models.CharField(
        max_length=200,
        help_text=
        'Введите жанр книги (например, научная фантастика, французская поэзия и т.д.).'
    )

    def __str__(self):
        """
            Строка для представления объекта модели (на сайте администратора и т. д.)
        """

        return self.name


class Book(models.Model):
    """
        Модель, представляющая книгу (но не конкретную копию книги).
    """

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Используется внешний ключ, поскольку у книги может быть только один автор, а у авторов может быть несколько книг.
    # Author как строку, а не как объект, потому что он еще не объявлен в файле.
    summary = models.TextField(max_length=1000,
                               help_text='Введите краткое описание книги')
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        help_text=
        '13-символьный <a href="https://www.isbn-international.org/content/what-isbn">номер ISBN'
    )
    genre = models.ManyToManyField(Genre,
                                   help_text='Выберите жанр для этой книги')

    language = models.ForeignKey('Language',
                                 on_delete=models.SET_NULL,
                                 null=True)

    # Используется ManyToManyField, потому что жанр может содержать много книг.  Книги могут охватывать множество жанров.
    # Класс жанра уже определен, поэтому мы можем указать объект выше.

    def __str__(self):
        """
            Строка для представления объекта Model.
        """
        return self.title

    def get_absolute_url(self):
        """
            Возвращает URL-адрес для доступа к определенному экземпляру книги.
        """

        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
            Создает строку для жанра.  Это необходимо для отображения жанра в Admin
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """
        Модель, представляющая конкретный экземпляр книги (т.е. который можно взять в библиотеке).
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text=
        'Уникальный идентификатор этой конкретной книги во всей библиотеке')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)

    LOAN_STATUS = (
        ('m', 'Не доступна'),  # 'Maintenance'
        ('o', 'Взять на руки'),  # 'On loan'
        ('a', 'Свободный'),  # 'Available'
        ('r', 'Занято'),  # 'Reserved'
    )

    status = models.CharField(max_length=1,
                              choices=LOAN_STATUS,
                              blank=True,
                              default='m',
                              help_text='Забронировать книгу')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """
            Строка для представления объекта Model
        """
        return '{0} ({1})'.format(self.id, self.book.title)

    @property
    def is_oberdue(self):
        if self.due_back and date.today() > self.due_back:
            return True

        return False


class Author(models.Model):
    """
        Модель, представляющая автора.
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
            Возвращает URL-адрес для доступа к конкретному экземпляру автора.
        """

        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
            Строка для представления объекта Model
        """

        return '{0}, {1}'.format(self.last_name, self.first_name)

    class Meta:
        ordering = ['last_name']


class Language(models.Model):
    """
        Модель, представляющая язык (например, английский, французский, японский и т. д.)
    """

    name = models.CharField(
        max_length=200,
        help_text=
        'Введите язык книги (например, английский, французский, японский и т. д.)'
    )

    def __str__(self):
        """
            Строка для представления объекта модели (на сайте администратора и т. д.)
        """

        return self.name
