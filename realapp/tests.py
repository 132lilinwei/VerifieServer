from django.test import TestCase
from django.utils import timezone
# Create your tests here.
from realapp.models import MyUser

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

