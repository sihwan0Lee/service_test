from django.urls import path
from .views import FindProduct, CreateProduct, DeleteProduct
urlpatterns = [
    path('/check/<int:product_id>', FindProduct.as_view()),
    path('/register', CreateProduct.as_view()),
    path('/del/<int:product_id>', DeleteProduct.as_view())
]
