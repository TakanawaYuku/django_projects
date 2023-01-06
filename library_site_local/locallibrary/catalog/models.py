from django.db import models
from django.shortcuts import reverse


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
