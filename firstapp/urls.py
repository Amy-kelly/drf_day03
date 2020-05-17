from django.urls import path

from firstapp import views

urlpatterns = {
    path("books/",views.BookAPIView.as_view()),
    path("books/<str:id>/",views.BookAPIView.as_view()),
    path("books1/",views.BookGenericAPIView.as_view()),
    path("books1/<str:pk>/",views.BookGenericAPIView.as_view()),
    path("books2",views.BookGenericViewSet.as_view({'get':'my_list','post':'my_create'})),
    path("books2/<str:pk>/",views.BookGenericViewSet.as_view({'get':'my_obj','post':'my_destroy'})),
}