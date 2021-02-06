from django.urls import path
from .views import LogIn, LogOut, CreateAccount, Myinfo

urlpatterns = [
    path('/signup', CreateAccount.as_view()),
    path('/signin', LogIn.as_view()),
    path('/logout', LogOut.as_view()),
    path('/myinfo', Myinfo.as_view()),
]
