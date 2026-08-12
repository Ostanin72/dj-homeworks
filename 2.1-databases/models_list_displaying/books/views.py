from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('books')

def books_view(request):
    template = 'books/books_list.html'

    context = {
        'books': Book.objects.all(),
    }
    return render(request, template, context)

def books_view_date(request, pub_date):
    template = 'books/book_date.html'
    books_on_this_date = Book.objects.filter(
        pub_date=pub_date
    ).order_by('name')
    current_book = books_on_this_date.first()
    previous_book = Book.objects.filter(
        pub_date__lt=current_book.pub_date
    ).order_by('-pub_date').first()
    next_book = Book.objects.filter(
        pub_date__gt=current_book.pub_date
    ).order_by('pub_date').first()

    context = {
        'books': books_on_this_date,
        'current_book': current_book,
        'previous_book': previous_book,
        'next_book': next_book,
    }

    return render(request, template, context)
