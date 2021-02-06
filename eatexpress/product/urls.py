from django.urls import path
from .views import ProductInfo, CreateProduct, DeleteProduct
urlpatterns = [
    path('/info/<int:product_id>', ProductInfo.as_view()),
    path('/register', CreateProduct.as_view()),
    path('/del/<int:product_id>', DeleteProduct.as_view())
]
