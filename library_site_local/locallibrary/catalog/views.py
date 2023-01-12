from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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
        status__exact='a').count

    num_authors = Author.objects.count(
    )  # в данной строчке Метод 'all()'  применён по умолчанию.

    # Количество жанров
    num_genre = Genre.objects.all().count()

    # Количество книг, которые содержат в своих заголовках какое-либо слово (без учёта регистра)
    num_book_title = Book.objects.values('title').count()

    # Количество посещений этого представления, подсчитанное в переменной сеанса.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

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
            'num_visits': num_visits,
        },
    )


class BookListView(generic.ListView):
    model = Book

    paginate_by = 5

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

    # def book_detail_view(request, pk):
    #     try:
    #         book_id = Book.objects.get(pk=pk)
    #     except Book.DoesNotExist:
    #         raise Http404("Book does not exist")

    #     #book_id=get_object_or_404(Book, pk=pk)

    #     return render(request,
    #                   'catalog/book_detail.html',
    #                   context={
    #                       'book': book_id,
    #                   })


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5


class AuthorDetailView(generic.DetailView):
    model = Author


@login_required
def my_view(request):
    pass


# class MyView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     redirect_field_name = 'redirect_to'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """

        Общий список книг на основе классов, предоставленных текущему пользователю.
    """

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(
            status='o').order_by('due_back')


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """
        перечислены все книги, предоставленные взаймы.  Видно только пользователям с разрешением can_mark_returned.
    """
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Если это POST-запрос, то обработайте данные формы
    if request.method == 'POST':

        # Создадим экземпляр формы и заполним его данными из запроса (binding):
        form = RenewBookForm(request.POST)

        # Проверяем правильность формы:
        if form.is_valid():
            # обрабатываем данные в form.cleaned_data по мере необходимости (здесь мы просто записываем их в поле модели due_back)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # перенаправление на новый URL:

            return HttpResponseRedirect(reverse('all-borrowed'))

    # Если это GET (или любой другой метод), создайте форму по умолчанию
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(
            weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
