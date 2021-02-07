"""
주문하기, 주문확인, 주문삭제 기능이 담겨있습니다.
"""
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
        """
        주문을 생성합니다.
        order_id : 입력받은 order_id를 이용하여 검증된 유저의 장바구니 여부를 확인합니다.
        product_id : 개별적으로 주문을하고 장바구니에 담길 상품의 id입니다.
        """
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

                return JsonResponse({'message': '주소를 등록해주세요'}, status=400)

            else:
                new_order = Order(
                    username_id=user_id
                )
                new_order.save()
                return JsonResponse({'message': '장바구니가 생성됬습니다'}, status=200)

        except KeyError:
            return JsonResponse({'error': '올바르지 않은 키 값'}, status=400)


class OrderListView(View):
    @member_verification
    def get(self, request, order_id):
        user_s_id = request.userid
        if Order.objects.filter(username_id=user_s_id).exists():  # 검증된 회원의 장바구니가 존재한다면
            username_id = Order.objects.get(username_id=user_s_id)
            if Order.objects.filter(id=order_id).exists():
                username_id_intable = Order.objects.get(
                    id=order_id).username_id
                if username_id == username_id_intable:
                    #   infos = OrderProduct.objects.filter(
                    #      order_id=order_id).values()
                    # orderinfo = [
                    #  {

                    #     'order_id': info.order_id,
                    #    'product_id': info.product_id,
                    #   'quantity': info.quantity
                    # }for info in infos
                    # ]
                    return JsonResponse({'orderinfo': "일치"}, status=200)
                return JsonResponse({'error': "본인과 일치하는 장바구니가 없습니다"}, status=400)
            return JsonResponse({'error': "장바구니를 확인해주세요"}, status=400)
        return JsonResponse({'error': "검증되지 않음."}, status=400)
        #   if user.level == 'admin':


class OrderDel(View):
    @ member_verification
    def post(self, request, order_id):
        """
        주문을 삭제합니다.
        인증된 유저아이디와 오더테이블의 유저네임 아이디가 같을때, 내 주문정보만을 가져올수 있게됩니다.
        order_id : 삭제할 장바구니의 id
        """
        user_s_id = request.userid
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
