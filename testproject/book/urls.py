from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<slug:slug>/', views.detail, name='detail'),
    re_path(r'add/$', views.book_add, name='book_add'),

]