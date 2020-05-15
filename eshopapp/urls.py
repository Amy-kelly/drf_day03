from django.urls import path

from eshopapp import views

urlpatterns = [
    path("products/",views.ProductAPIView.as_view()),
    path("products<str:id>/",views.ProductAPIView.as_view())
]