import time

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from .models import Message

base = "chat/templates/chat/"


class HomeView(View):
    def get(self, request):
        return render(request, base + "main.html")


def jsonfun(request):
    time.sleep(2)
    stuff = {
        'first': 'first thing',
        'second': 'second thing'
    }
    return JsonResponse(stuff)


def log(request):
    return render(request, base + "login.html")


def log_in(request):
    if request.method == "POST":
        name = request.POST["name"]
        password = request.POST["password"]

        user = authenticate(request, username=name, password=password)

        if user is not None:
            login(request, user)
            # return redirect(reverse("main"))
            return redirect(reverse("chat:main"))
        else:
            messages.add_message(request, messages.INFO, 'Invalid credentials.')
            return redirect(reverse("chat:main"))


class TalkMain(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, base + "talk.html")

    def post(self, request):
        message = Message(text=request.POST.get('message'), owner=request.user)
        message.save()
        return redirect(reverse("chat:talk"))


class TalkMessages(LoginRequiredMixin, View):
    def get(self, request):
        messages = Message.objects.all().order_by('-created_at')
        results = []
        for message in messages:
            result = [message.text, naturaltime(message.created_at)]
            results.append(result)
        return JsonResponse(results, safe=False)
        # Its default Content-Type header is set to application/json.
        # The first parameter, data, should be a dict instance. If the safe parameter is set to False (see below) it can be any JSON-serializable object.
        # The safe boolean parameter defaults to True. If it’s set to False, any object can be passed for serialization (otherwise only dict instances are allowed). If safe is True and a non-dict object is passed as the first argument, a TypeError will be raised.
