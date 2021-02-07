"""유저의 회원가입, 로그인, 로그아웃, 내 정보 확인, 내 정보 수정 뷰들이 담겨있습니다."""
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
        """
        회원가입을 진행합니다. 이메일과, 닉네임의 중복을 막습니다.

        """
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "이미 존재하는 이메일입니다"}, status=400)
            if User.objects.filter(nickname=data['nickname']).exists():
                return JsonResponse({"message": "이미 존재하는 닉네임입니다"}, status=400)

            password_crypt = bcrypt.hashpw(
                data['password'].encode('utf-8'), bcrypt.gensalt())
            password_crypt = password_crypt.decode('utf-8')

            new_user = User(
                # abstractuser 기본제공하는 username
                username=data['username'],
                nickname=data['nickname'],
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
        """
        로그인을 진행합니다.
        email=data['email'] : 입력받은 이메일
        checkpw() : 함수를 이용해 db의 비밀번호와 입력받은 비밀번호의 일치성 여부를 확인합니다.
        그리고 프론트에게 토큰을 전달하면 로그인이 끝납니다.

        """
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode(
                        {'user_id': user.id}, SECRET_KEY, algorithm=HASH)

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
        """
        개인정보를 수정합니다.
        아이디(이메일)은 보통 수정못하게 하였습니다.
        username, nickname, phone_number 은 중복이 불가하게하여 타인의 정보를 접근못하게 하였습니다.
        """
        user_id = request.userid
        try:
            data = json.loads(request.body)
            username = data['username']
            nickname = data['nickname']
            # password=password_crypt,
            phone_number = data['phone_number']
            address = data['address']
            if User.objects.filter(id=user_id).exists():
                User.objects.filter(id=user_id).update(
                    username=username, nickname=nickname, phone_number=phone_number, address=address)
                return JsonResponse({"message": "유저정보가 변경되었습니다"}, status=200)
        except KeyError:
            return JsonResponse({'error': '올바르지 않은 키 값'}, status=400)
        except IntegrityError:
            return JsonResponse({'error': '이미 존재하는 값'}, status=400)

    @member_verification
    def get(self, request):
        """
        개인정보를 확인합니다.
        """
        user_id = request.userid
        info = User.objects.get(id=user_id)
        my_info = []

        j = {
            'username': info.username,
            'nickname': info.nickname,
            'email': info.email,
            'phone_number': info.phone_number,
            'address': info.address,
            'gender': info.gender
        }
        my_info.append(j)
        return JsonResponse({'info': my_info}, status=200)
