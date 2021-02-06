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
    # 해당 유저가 존재할시 해당유저 정보를 지우고 , 새로운 값을 저장하게 함.
    @member_verification
    def post(self, request):
        user = request.user
        if User.objects.filter(username=user).exists():
            User.objects.get(username=user).delete()

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
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({'error': '올바르지 않은 키 값'}, status=400)

    @member_verification
    def get(self, request):
        user = request.user
        info = User.objects.get(username=user)
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
