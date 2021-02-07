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
        user_id = request.userid
        try:
            if Order.objects.filter(username_id=user_id).exists():
                user_address = User.objects.get(id=user_id).address
                if user_address:
                    if Order.objects.filter(id=order_id).exists():
                        if Product.objects.filter(id=product_id).exists():
                            order_id = Order.objects.get(id=order_id)
                            product_id = Product.objects.get(id=product_id)
                            new_order = OrderProduct(
                                order=order_id,
                                product=product_id,
                                quantity=data['quantity']
                            )
                            new_order.save()
                            return JsonResponse({'message': "장바구니에 담겼습니다"}, status=200)
                        return JsonResponse({'message': '해당 상품은 존재하지 않습니다'}, status=400)
                return JsonResponse({'message': '주소를 변경해주세요'}, status=400)

            else:
                new_order = Order(
                    username_id=user_id
                )
                new_order.save()
                return JsonResponse({'message': '장바구니가 생성됬습니다'}, status=200)
            # return JsonResponse({'message': '장바구니를 먼저 생성하세요'}, status=400)

        except KeyError:
            return JsonResponse({'error': '올바르지 않은 키 값'}, status=400)


class OrderListView(View):
    @member_verification
    def get(self, request, user_id):
        user = request.user
        user_s_id = request.userid
        # if User.objects.filter(username=user).exists():
        #   if user.level == 'admin':


class OrderDel(View):
    @member_verification
    def post(self, request, order_id):
        user_s_id = request.userid
        # 인증된 유저아이디와 오더테이블의 유저네임 아이디가 같을때, 내 주문정보만을 가져올수 있게됌.
        try:
            user_id = Order.objects.get(id=order_id).username_id
            if user_s_id == user_id:
                Order.objects.get(id=order_id).delete()
                return JsonResponse({'message': "주문 삭제 완료"}, status=200)
            return JsonResponse({'error': '본인의 주문만 취소 가능합니다..'}, status=401)
        except KeyError:
            return JsonResponse({'error': '장바구니가 없는 회원이십니다.'}, status=401)
        # except DoesNotExist:
         #   return JsonResponse({'error': '장바구니가 없는 회원이십니다.'}, status=401)
