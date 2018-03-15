from django.test import TestCase
from django.utils import timezone
# Create your tests here.
from realapp.models import MyUser
from realapp.views import appres_too_frequent, appres_fatal_error, appres_veri_fail

# Create your tests here.
class UserModelTest(TestCase):
    def test_time(self):
        result = True
        for user in MyUser.objects.all():
            if user.create_date > timezone.now():
                result = False
        return self.assertIs(result, True)

    def test_username(self):
        list = []
        for user in MyUser.objects.all():
            list.append(user.username)

        myset = set(list)
        return self.assertIs(len(list),len(myset))

import unittest
from django.test import Client

class ClientTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_login(self):
        self.setUp()
        #No account
        response = self.client.post('/login/basic/', {'username': 'nosuch', 'password': 'smith'})
        print(response)
        self.assertNotEqual(response, "SUCCESS")

        #Wrong password
        response = self.client.post('/login/basic/', {'username': 'lilinwei', 'password': 'smith'})
        self.assertNotEqual(response, "SUCCESS")

    def test_registration(self):
        self.setUp()
        #Not enough info
        response = self.client.post('/registration/basic/', {'username': 'nosuch', 'password': 'smith'})
        self.assertNotEqual(response, "SUCCESS")

        #correct
        response = self.client.post('/registration/basic/', {'username': 'test', 'password': 'test', 'nric':'123','email':'llw19970903@live.com','phone_number':'82838552'})
        self.assertEqual(response,"SUCCESS")

        #wrong verification code
        response = self.client.post('/registration/emailveri/',{'randomcode':'0000'})
        self.assertEqual(response, appres_veri_fail)

    def test_attack(self):
        self.setUp()
        #correct login
        response = self.client.post('/login/basic/', {'username': 'lilinwei', 'password': 'lilinwei'})
        self.assertEqual(response, "SUCCESS")

        #attack
        for i in range(100):
            response = self.client.post('login/email')
            self.assertEqual(response, appres_too_frequent)

    def test_faulty_access(self):
        self.setUp()
        response = self.client.post('/login/photo/')
        self.assertEqual(appres_fatal_error)

