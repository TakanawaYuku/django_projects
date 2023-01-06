from django.db import models


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
