import json
import bcrypt
import jwt

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError

from eatexpress.settings import SECRET_KEY, HASH
from user.models import User

from eatexpress.decorator import member_verification


class CreateAccount(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "이미 존재하는 이메일입니다"}, status=400)

            password_crypt = bcrypt.hashpw(
                data['password'].encode('utf-8'), bcrypt.gensalt())
            password_crypt = password_crypt.decode('utf-8')

            new_user = User(
                # abstractuser 기본제공하는 username
                username=data['username'],
                email=data['email'],
                password=password_crypt,
                phone_number=data['phone_number'],
                address=data['address'],
                gender=['gender']
            )
            new_user.save()
            return JsonResponse({'message': '가입을 축하합니다'}, status=200)
        except IntegrityError:
            return JsonResponse({"error": "이미 존재하는 회원정보"}, status=400)

        except KeyError:
            return JsonResponse({'error': '올바르지 않은 키 값'}, status=400)


class LogIn(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode(
                        {'user_id': user.id}, SECRET_KEY, algorithm=HASH)
                    # token = token.decode('utf-8')

                    return JsonResponse({"token": token}, status=200)
                else:
                    return JsonResponse({"message": "틀린 비밀번호"}, status=401)
            return JsonResponse({"message": "존재하지 않는 이메일아이디"}, status=401)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=401)


class LogOut(View):
    @member_verification
    def post(self, request):
        pass


class Myinfo(View):
    @member_verification
    def post(self, request):
        user_id = request.userid

        # 아이디(이메일)은 보통 수정못하는 점을 반영, 주문을 위한 주소변경을 중점으로 다룸.
        try:
            data = json.loads(request.body)
            username = data['username']
            # password=password_crypt,
            phone_number = data['phone_number']
            address = data['address']
            if User.objects.filter(id=user_id).exists():
                User.objects.filter(id=user_id).update(
                    username=username, phone_number=phone_number, address=address)
                return JsonResponse({"message": "유저정보가 변경되었습니다"}, status=200)
        except KeyError:
            return JsonResponse({'error': '올바르지 않은 키 값'}, status=400)

    @member_verification
    def get(self, request):
        user_id = request.userid
        info = User.objects.get(id=user_id)
        my_info = []

        j = {
            'username': info.username,
            'email': info.email,
            'phone_number': info.phone_number,
            'address': info.address,
            'gender': info.gender
        }
        my_info.append(j)
        return JsonResponse({'info': my_info}, status=200)
