import jwt
import json
import requests
from django.http import JsonResponse
from eatexpress.settings import SECRET_KEY, HASH
from user.models import User


def member_verification(func):
    def wrapper(self, request, *args, **kwargs):
        token_from_Front = request.headers.get('Authorization', None)
        if token_from_Front:
            #print(token_from_Front, "token from front")
            try:
                payload = jwt.decode(
                    token_from_Front, SECRET_KEY, algorithms=HASH)
                user_id = payload['user_id']
                #print(payload, 'payload')
                user = User.objects.get(pk=user_id)

                # 로그인한 회원만 이용할수 있는 서비스의 view에 쓰일 변수.
                request.user = user
                request.userid = payload['user_id']
                print(request.user, request.userid)

            except jwt.DecodeError:
                return JsonResponse({"message": "올바르지 않은 토큰"}, status=401)
            except User.DoesNotExist:
                return JsonResponse({"message": "존재하지 않는 회원"}, status=401)
            return func(self, request, *args, **kwargs)
        else:
            return JsonResponse({"message": "로그인이 필요합니다"}, status=401)

    return wrapper


# def staff_verification(func):
 #   @member_verification
  #  def wrapper(self, request):
   #     user = request.user
    #    if User.objects.filter(username=user).exists():
    #       if user.level == 'admin':
    #          admin = user
    #     return JsonResponse({"message": "you are admin"}, status=200)
    # return JsonResponse({"message": "you are not admin"}, status=401)
    # return wrapper
