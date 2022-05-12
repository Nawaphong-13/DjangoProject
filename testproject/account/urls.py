from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
