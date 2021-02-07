from django.urls import path
from .views import OrderMake, OrderDel
urlpatterns = [

    path('/mk/<int:order_id>/<int:product_id>', OrderMake.as_view()),
    path('/del/<int:order_id>', OrderDel.as_view())
]
