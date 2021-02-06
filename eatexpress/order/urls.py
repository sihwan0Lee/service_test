from django.urls import path
from .views import OrderMake
urlpatterns = [
    path('/mk/<int:order_id>/<int:product_id>', OrderMake.as_view())
]
