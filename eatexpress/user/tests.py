from django.db import transaction
from unittest.mock import patch, MagicMock
from django.test import TransactionTestCase, Client
from models import User
import json


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


class UserTest(TransactionTestCase):
    def setUp(self):
        User.objects.create(
            username='지수',
            email='sh@naver.com',
            password='1234',
            phone_number='010-1234-1234',
            address='서울시',
            gender=''
        )

    def tearDown(self):
        User.objects.filter(name='아이유').delete()

    @patch("account.views.requests")
    def test_user_naver_account(self, mocked_requests):
        c = Client()

        class MockedResponse:
            def json(self):
                return {
                    "response": {
                        'username': '지수',
                        'email': 'sh@naver.com',
                        'password': '1234',
                        'phone_number': '010-1234-1234',
                        'address': '서울시',
                        'gender': ''
                    }
                }
        mocked_requests.get = MagicMock(return_value=MockedResponse())

        response = c.get("/account/sign-in",
                         {"content_type": "applications/json"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS'})
