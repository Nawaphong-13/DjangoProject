from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm

# Create your views here.

def writer(request):
    form = ArticleForm()
    username = None
    if request.method == 'POST':
        # if request.user.is_authenticated():
        username = request.user.username
        print(username)

        form = ArticleForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['book'])
            form.save()

            return redirect('book:index')

    return render(request, 'article/writer.html', {'form':form})
