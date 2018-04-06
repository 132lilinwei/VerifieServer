from django.test import TestCase
from django.utils import timezone
from django.test import override_settings
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
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_noaccount(self):
        # Nonexistent account
        self.setUp()
        response = self.client.post('/realapp/login/basic/', {'username': 'nosuch', 'password': 'smith'})
        self.assertEqual(response.content.decode('utf-8'), "NO SUCH USER")

    def test_login_wrong_password(self):
        #Wrong password
        self.setUp()
        response = self.client.post('/realapp/login/basic/', {'username': 'lilinwei', 'password': 'smith'})
        self.assertNotEqual(response.content, "SUCCESS")

    def test_incomplete_registration(self):
        self.setUp()
        #Not enough info
        response = self.client.post('/realapp/registration/basic/', {'username': 'nosuch', 'email': '', 'nric': '', 'password': 'smith', 'phone_number': '82838552'})
        self.assertNotEqual(response.content, "SUCCESS")
    
    def test_correct_registration(self):
        #correct
        self.setUp()
        response = self.client.post('/realapp/registration/basic/', {'username': 'test', 'password': 'test', 'nric':'123','email':'llw19970903@live.com','phone_number':'82838552'})
        self.assertEqual(response.content.decode('utf-8'), "SUCCESS")

    def test_wrong_email_code(self):
        #wrong email verification code
        self.setUp()
        response = self.client.post('/realapp/registration/emailveri/',{'randomcode':'0000'})
        self.assertNotEqual(response.content, "SUCCESS")

    def test_wrong_sms_code(self):
        #wrong sms verification code
        self.setUp()
        response = self.client.post('/realapp/registration/phoneveri/',{'randomcode':'0000'})
        self.assertNotEqual(response.content, "SUCCESS")

    def test_wrong_digi_code(self):
        #wrong digicode code
        self.setUp()
        response = self.client.post('/realapp/registration/digicardveri/',{'randomcode':'0000'})
        self.assertNotEqual(response.content, "SUCCESS")

    def test_attack(self):
        self.setUp()
        #correct login
        response = self.client.post('/realapp/login/basic/', {'username': 'lilinwei', 'password': 'lilinwei'})
        self.assertEqual(response.content.decode('utf-8'), "NO SUCH USER")

        # ddos attack
        for i in range(100):
            response = self.client.post('/realapplogin/email')
            self.assertNotEqual(response.content, "SUCCESS")

    def test_faulty_access(self):
        self.setUp()
        response = self.client.post('/realapp/login/photo/')
        self.assertNotEqual(response.content, "SUCCESS")

    def test_location(self):
        self.setUp()
        response = self.client.post('/login/', {'username': 'llw19970903@live.com', 'password': 'linwei'}, REMOTE_ADDER="50.233.137.38")

