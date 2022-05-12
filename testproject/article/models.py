from django.db import models
from book.models import Book
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Article(models.Model):
    book = models.ForeignKey(Book, related_name='books', on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book.name
