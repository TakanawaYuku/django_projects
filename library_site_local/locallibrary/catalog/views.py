from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre, Language
from django.views import generic
from django.http import Http404


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
        status__exact='a').count

    num_authors = Author.objects.count(
    )  # в данной строчке Метод 'all()'  применён по умолчанию.

    # Количество жанров
    num_genre = Genre.objects.all().count()

    # Количество книг, которые содержат в своих заголовках какое-либо слово (без учёта регистра)
    num_book_title = Book.objects.values('title').count()

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context

    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instance': num_instance,
            'num_instance_available': num_instance_available,
            'num_authors': num_authors,
            'num_genre': num_genre,
            'num_book_title': num_book_title,
        },
    )


class BookListView(generic.ListView):
    model = Book

    paginate_by = 10

    # def get_queryset(self):
    #     return Book.objects.filter(
    #         title__icontains=''
    #     )  # Получить 5 книг, содержащих 'war' в заголовке

    # def get_context_data(self, **kwargs):

    #     # В первую очередь получаем базовую реализацию контекста
    #     context = super(BookListView, self).get_context_data(**kwargs)

    #     # Добавляем новую переменную к контексту и инициализируем её некоторым значением
    #     context['some_date'] = 'This is just some data'

    #     return context


class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(request, pk):
        try:
            book_id = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Book does not exist")

        #book_id=get_object_or_404(Book, pk=pk)

        return render(request,
                      'catalog/book_detail.html',
                      context={
                          'book': book_id,
                      })
