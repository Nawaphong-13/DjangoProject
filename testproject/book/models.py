from django.utils.html import format_html
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


BOOK_LEVEL_CHOICE = (
    ('B', 'Basic'),
    ('M', 'Medium'),
    ('A', 'Advance'),)


class Book(models.Model):

    code = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    author = models.ManyToManyField(Author, blank=True)
    level = models.CharField(max_length=20, null=True, blank=True, choices=BOOK_LEVEL_CHOICE)
    image = models.FileField(upload_to='upload/', null=True, blank=True)
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']  # ติดลบคือ มากไปน้อย
        verbose_name_plural = 'Book'

    def show_image(self):
        if self.image:
            return format_html('<img src="%s" height="50px">' % self.image.url)
        return ''
    show_image.allow_tags = True
    show_image.short_description = 'Image'

    def get_comment_count(self):
        return self.bookcomment_set.count()


    def __str__(self):
        return self.name


class BookComment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    rating = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Book Comment'  # น้อยไปมาก

    def __str__(self):
        return self.comment
