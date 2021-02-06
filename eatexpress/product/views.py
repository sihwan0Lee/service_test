import json

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from product.models import Product
from user.models import User
from django.db import IntegrityError

from eatexpress.decorator import member_verification

# Create your views here.


class ProductInfo(View):
    @member_verification
    def get(self, request, product_id):
        user = request.user
        if User.objects.filter(username=user).exists():
            if user.level == 'admin':
                try:
                    if Product.objects.filter(id=product_id).exists():
                        product = Product.objects.get(id=product_id)

                        product = {
                            'name': product.name,
                            'manufacturer': product.manufacturer,
                            'stock': product.stock,
                            'unit_price': product.unit_price,
                            'expiration_date': product.expiration_date
                        }

                        return JsonResponse({'info': product}, status=200)
                    return JsonResponse({"error": "존재하지 않는 제품"}, status=400)
                except KeyError:
                    return JsonResponse({'error': '올바르지 않은 키 값'}, status=400)
            return JsonResponse({'error': '제한된 서비스'}, status=400)

    @member_verification
    def post(self, request, product_id):
        user = request.user
        if User.objects.filter(username=user).exists():
            if user.level == 'admin':
                try:
                    data = json.loads(request.body)
                    name = data['name']
                    manufacturer = data['manufacturer']
                    stock = data['stock']
                    unit_price = data['unit_price']
                    expiration_date = data['expiration_date']
                    if Product.objects.filter(id=product_id).exists():
                        Product.objects.filter(id=product_id).update(
                            name=name, manufacturer=manufacturer, stock=stock, unit_price=unit_price, expiration_date=expiration_date)
                        return JsonResponse({"message": "상품정보가 변경되었습니다"}, status=200)
                except KeyError:
                    return JsonResponse({'error': '올바르지 않은 키 값'}, status=400)
            return JsonResponse({'error': '제한된 서비스'}, status=400)


class CreateProduct(View):
    @ member_verification
    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        if User.objects.filter(username=user).exists():
            if user.level == 'admin':

                try:
                    if Product.objects.filter(name=data['name']).exists():
                        return JsonResponse({"message": "이미 등록된 상품입니다"}, status=400)

                    new_product = Product(
                        name=data['name'],
                        manufacturer=data['manufacturer'],
                        stock=data['stock'],
                        unit_price=data['unit_price'],
                        expiration_date=data['expiration_date']

                    )
                    new_product.save()
                    return JsonResponse({"error": "상품이 등록되었습니다"}, status=200)
                except IntegrityError:
                    return JsonResponse({"error": "이미 존재하는 정보"}, status=401)

                except KeyError:
                    return JsonResponse({'error': '올바르지 않은 키 값'}, status=401)
        return JsonResponse({"message": "you are not admin"}, status=401)


class DeleteProduct(View):
    @ member_verification
    def delete(self, request, product_id):
        user = request.user
        if User.objects.filter(username=user).exists():
            if user.level == 'admin':

                if Product.objects.filter(id=product_id).exists():
                    Product.objects.get(id=product_id).delete()
                    return JsonResponse({'message': "제품 삭제 완료"}, status=200)
            return JsonResponse({'error': '제한된 서비스'}, status=400)
