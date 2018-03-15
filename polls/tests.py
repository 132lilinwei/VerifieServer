# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .models import Question


# Create your tests here.
class QuestionModelTest(TestCase):
    def haha(self):
        return self.assertIs(True,True)    #python manage.py test polls
