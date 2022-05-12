from django.urls import path, re_path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('writer/', login_required(views.writer, login_url='account:login'), name='writer'),
    # path('writer/', views.writer, name='writer'),
]
