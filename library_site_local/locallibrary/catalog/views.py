from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre, Language


# Create your views here.
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов

    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()

    # Доступные книги (статус = 'a')
    num_instance_available = BookInstance.objects.filter(
        status_exact='a').count

    num_authors = Author.objects.count(
    )  # в данной строчке Метод 'all()'  применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context

    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instance': num_instance,
            'num_instance_available': num_instance_available,
            'num_authors': num_authors
        },
    )
