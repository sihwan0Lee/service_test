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
    def post(self, request, order_id, product_id):
        data = json.loads(request.body)
        user = request.user
        # 주문id가 있는지, 없으면 주문id생성부터 (장바구니 생성)
        try:
            if Order.objects.filter(username_id=user):
                if Product.objects.filter(id=product_id):

                    new_order = OrderProduct(

                        order=data['order_id'],
                        product=data['product_id'],
                        quantity=data['quantity']

                    )
                    new_order.save()
            else:
                Order.objects.create(id=order_id, username_id=user.id)
            return JsonResponse({'message': '장바구니를 먼저 생성하세요'}, status=200)
        # except IntegrityError:
            # return JsonResponse({"error": "이미 존재하는 회원정보"}, status=400)

        except KeyError:
            return JsonResponse({'error': '올바르지 않은 키 값'}, status=400)
