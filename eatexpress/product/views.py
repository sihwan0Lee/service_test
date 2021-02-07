"""
상품의 등록, 상품확인, 상품수정, 상품삭제 뷰들이 담겨있습니다.
"""
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
        """
        product_id : 정보를 확인하려는 상품의 id
        """

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
        """
        상품의 정보를 수정합니다.
        product_id : 정보를 변경하고자하는 상품의 ID
        update()함수를 이용했습니다.
        """
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
        """
        상품을 등록합니다
        """
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
        return JsonResponse({"message": "제한된 서비스"}, status=401)


class DeleteProduct(View):
    @ member_verification
    def delete(self, request, product_id):
        """
        상품을 삭제합니다.
        product_id : 삭제할 상품의 id
        """
        user = request.user
        if User.objects.filter(username=user).exists():
            if user.level == 'admin':

                if Product.objects.filter(id=product_id).exists():
                    Product.objects.get(id=product_id).delete()
                    return JsonResponse({'message': "제품 삭제 완료"}, status=200)
                return JsonResponse({'error': '존재하지않는 상품'}, status=400)
            return JsonResponse({'error': '제한된 서비스'}, status=400)
