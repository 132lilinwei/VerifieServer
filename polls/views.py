# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from polls.models  import Question,Choice
from django.shortcuts import get_object_or_404
from django.urls import reverse
# Create your views here.


def index(request):
    question_set = Question.objects.all()
    return render(request, 'polls/index.html',{'question_set' : question_set})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request,question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/results.html', {"question":question})


def vote(request,question_id):
    question = get_object_or_404(Question,pk = question_id)
    try :
        choice = question.choice_set.get(pk = request.POST["choice"])
    except(KeyError,Choice.DoesNotExist):
        return render(request,"polls/detail.html" ,{
            "question":question,
            "error_message" : "Wrong Input"
        })
    choice.votes += 1;
    choice.save();

    return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))