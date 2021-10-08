from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from game.models import *

from django.utils import timezone


def log_in(request):
    template = loader.get_template('authenticator/loginnew.html')
    context = {
        'user': request.user,
        'next': request.GET.get('next'),
    }
    return HttpResponse(template.render(context, request))

def log_out(request):
    logout(request)
    response = HttpResponse("You have been logged out successfully")
    response.delete_cookie('access_token')
    return response

def check(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        if not hasattr(user, "player"):
            create_new_player(user)

        return redirect('game:index')
    else:
        return redirect('auth:login')
# Create your views here.

def create_new_player(user):
    p = Player(user=user)
    p.save()

    knife = Item(data=ItemMeta.objects.get(id=1), player=p)
    knife.save()
    phone = Item(data=ItemMeta.objects.get(id=2), player=p)
    phone.save()
    high_heels = Item(data=ItemMeta.objects.get(id=3), player=p)
    high_heels.save()
    beginning = Event.objects.get(desc="Beginning")
    ce = CausedEvent(event=beginning, player=p, time=timezone.now())
    ce.save()
