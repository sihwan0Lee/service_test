import json

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from order.models import Order, OrderProduct
from product.models import Product
from user.models import User
from django.db import IntegrityError

from eatexpress.decorator import member_verification


class OrderMake(View):
    @member_verification
    def post(self, request):
        data = json.loads(request.body)
        user_id = request.userid
        try:
            if Order.objects.filter(id=user_id).exists():
                # if Product.objects.filter(id=product_id):
                return JsonResponse({'message': '장바구니는 있네'}, status=200)
                # new_order = OrderProduct(

                #   order=data['user_id'],
                #  product=data['product_id'],
                # quantity=data['quantity']

                # )
                # new_order.save()
            else:
                new_order = Order(
                    username_id=user_id
                )
                new_order.save()
                return JsonResponse({'message': '장바구니가 생성됬습니다'}, status=200)
            return JsonResponse({'message': '장바구니를 먼저 생성하세요'}, status=200)
        # except IntegrityError:
            # return JsonResponse({"error": "이미 존재하는 회원정보"}, status=400)

        except KeyError:
            return JsonResponse({'error': '올바르지 않은 키 값'}, status=400)
