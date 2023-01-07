from django.contrib import admin
from .models import Author, Book, BookInstance, Language, Genre

# Register your models here.
admin.register(Book)
admin.register(Author)
admin.register(Genre)
admin.register(BookInstance)
admin.register(Language)
