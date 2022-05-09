from django.contrib import admin
from .models import Category, Author, Book, BookComment

# Register your models here.

class BookCommentStackedInline(admin.StackedInline):
    model = BookComment

class BookCommentTabularInline(admin.TabularInline):
    model = BookComment
    extra = 2



class BookAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'price', 'level', 'category', 'published', 'show_image']
    list_filter = ['published']
    search_fields = ['code', 'name']
    prepopulated_fields = {'slug': ['name']}
    fieldsets = (
        (None, {'fields': ['code', 'name', 'slug', 'description', 'level', 'image', 'price', 'published']}),
        ('Category', {'fields': ['category',
         'author'], 'classes': ['collapse']}),
    )
    inlines = [ BookCommentTabularInline ]


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book, BookAdmin)
