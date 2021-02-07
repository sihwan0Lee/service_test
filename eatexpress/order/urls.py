from django.urls import path
from .views import OrderMake, OrderDel, OrderListView
urlpatterns = [

    path('/mk/<int:order_id>/<int:product_id>', OrderMake.as_view()),
    path('/del/<int:order_id>', OrderDel.as_view()),
    path('/list/<int:order_id>', OrderListView.as_view())
]
