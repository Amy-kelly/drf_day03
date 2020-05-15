from django.urls import path

from bookapp import views

urlpatterns = [
    path("books/",views.BookAPIView.as_view()),
    path("books/<str:id>/",views.BookAPIView.as_view()),
    path("books2/",views.BookAPIView2.as_view()),
    path("books2/<str:id>/",views.BookAPIView2.as_view()),
]