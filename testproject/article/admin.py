from django.contrib import admin
from .models import Article

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['book', 'created_at', 'upload_to']

admin.site.register(Article, ArticleAdmin)