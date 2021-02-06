import json

from django.test import TestCase, Client

from .models import User
# class UserSetUp(TestCase):
#    def setup(self):
#        User.objects.create(
# username='지수',
#           email='sh@naver.com',
#           password='1234',
#           phone_number='010-3333-4444',
#           address='서울시',
#           gender=''
#       )

#   def tearDown(self):
#       User.objects.filter(name='지수').delete()


class SignUp(TestCase):
    def test_signup(self):
        client = Client()

        data = {
            'username': '지수',
            'email': 'sh@naver.com',
            'password': '1234',
            'phone_number': '010-1234-1234',
            'address': '서울시',
            'gender': ''
        }
        response = client.post(
            '/user/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "success"})
