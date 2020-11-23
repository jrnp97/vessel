import time

from django.test import TestCase

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import status

User = get_user_model()


class TestJWTLogin(TestCase):
    AUTH_API = '/auth/api/v1'
    JWT_LOGIN = '{prefix}/token/'
    JWT_VERIFY = '{prefix}/token/verify/'
    JWT_REFRESH = '{prefix}/token/refresh/'

    def setUp(self) -> None:
        self.cred = {
            'username': 'test_api',
            'password': 'test_pwd',
        }
        self.user = User.objects.create_user(**self.cred)

    def test_jwt_login_and_verify(self):
        response = self.client.post(
            path=self.JWT_LOGIN.format(
                prefix=self.AUTH_API,
            ),
            data=self.cred,
        )
        self.assertContains(
            response=response,
            status_code=status.HTTP_200_OK,
            text='access',
        )
        self.assertContains(
            response=response,
            status_code=status.HTTP_200_OK,
            text='refresh',
        )
        data = response.json()
        response = self.client.post(
            path=self.JWT_VERIFY.format(
                prefix=self.AUTH_API,
            ),
            data={
                'token': data['access'],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        time.sleep(settings.JWT_TOKEN_LIFETIME_SECONDS)
        response = self.client.post(
            path=self.JWT_VERIFY.format(
                prefix=self.AUTH_API,
            ),
            data={
                'token': data['access'],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_login_and_refresh(self):
        response = self.client.post(
            path=self.JWT_LOGIN.format(
                prefix=self.AUTH_API,
            ),
            data=self.cred,
        )
        self.assertContains(
            response=response,
            status_code=status.HTTP_200_OK,
            text='access',
        )
        self.assertContains(
            response=response,
            status_code=status.HTTP_200_OK,
            text='refresh',
        )
        data = response.json()
        time.sleep(settings.JWT_TOKEN_LIFETIME_SECONDS)
        response = self.client.post(
            path=self.JWT_VERIFY.format(
                prefix=self.AUTH_API,
            ),
            data={
                'token': data['access'],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(
            path=self.JWT_REFRESH.format(
                prefix=self.AUTH_API,
            ),
            data={
                'refresh': data['refresh'],
            }
        )
        self.assertContains(
            response=response,
            status_code=status.HTTP_200_OK,
            text='access',
        )
        data = response.json()
        response = self.client.post(
            path=self.JWT_VERIFY.format(
                prefix=self.AUTH_API,
            ),
            data={
                'token': data['access'],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)