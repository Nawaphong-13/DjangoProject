from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from slugify import slugify
from .forms import BookForm


def index(request):
    categories = Category.objects.all()
    books = Book.objects.filter(published=True)

    category_id = request.GET.get('categoryid')
    if category_id:
        books = books.filter(category_id=category_id)

    paginator = Paginator(books, 5)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return render(request, 'book/index.html', {
        'books': books,
        'categories': categories,
        'category_id': category_id,
    })


def detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'book/detail.html', {
        'book': book,
    })


def book_add(request):
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.slug = slugify(book.name)
            book.published= True
            book.save()
            form.save_m2m()
            messages.success(request, 'Save success')
            return redirect('book:index')
        messages.error(request, 'Save failed!')
    return render(request, 'book/add.html', {
        'form': form,
    })
