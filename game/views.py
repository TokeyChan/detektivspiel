from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
#from django.contrib.auth.models import User

from game.models import *
from game import event_checker

from django.utils import timezone
from datetime import datetime, timedelta
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def index(request):
    if request.user == None:
        logout(request)
    elif not hasattr(request.user, "player"):
        logout(request)
    event_checker.check_items(request.user.player)

    template = loader.get_template('game/main.html')
    context = {
        "player":request.user.player,
        "places":Place.objects.all(),
        "phone":request.user.player.item_set.filter(data__name="Handy")[0]
    }

    response = HttpResponse(template.render(context, request))

    value = request.COOKIES.get('access_token')
    if value is None:
        response.set_cookie('access_token', 'xb7a3c5bnepssklp')
    return response

@login_required
def place(request, name):
    event_checker.check_items(request.user.player)

    template = loader.get_template('game/place.html')
    place = Place.objects.get(name=name)
    if name == "bank":
        setup_finished = request.user.player.causedevent_set.filter(event__desc="Insp_Bank")[0].finished
    else:
        setup_finished = True

    context = {
        "place": place,
        "player": request.user.player,
        "setup_finished": setup_finished,
        "met_honey": True if Event.objects.get(desc="Met_Honey") in request.user.player.caused_events() else False,
        "met_sophia": True if Event.objects.get(desc="Chef:Sophia") in request.user.player.caused_events() else False
    }
    return HttpResponse(template.render(context, request))

@login_required
def decision(request):
    e = Event.objects.get(desc="Open_Decision")
    if not e in request.user.player.caused_events():
        event_checker.cause_event(e, request.user.player)
    template = loader.get_template('game/decision.html')
    return HttpResponse(template.render({}, request))

@login_required
def result(request):
    if not request.user.player.has_finished():
        score = 0
        correct = 0
        correct_persons = ['sophia', 'honey']
        for chosen in request.POST.getlist('chosen'):
            if chosen in correct_persons:
                score += 1
                correct += 1
            else:
                score -= 1
        request.user.player.final_score = score
        request.user.player.save()
        if score <= 0 and correct == 0:
            e = Event.objects.get(desc="Finished_Failure")
        elif score <= 0 and correct != 0:
            e = Event.objects.get(desc="Finished_Mediocre")
        elif score == 1:
            e = Event.objects.get(desc="Finished_Good")
        elif score == 2:
            e = Event.objects.get(desc="Finished_Perfect")
        else:
            request.user.player.final_score = None
            request.user.player.save()
        e2 = Event.objects.get(desc="Explanation")
        event_checker.cause_event(e, request.user.player)
        event_checker.cause_event(e2, request.user.player)
    return redirect('game:index')
# JS REQUESTS SIND HIER:

def items(request, name):
    return_dict = {}
    if name == "knife":
        knife_data = ItemMeta.objects.get(name="Messer")
        knife = request.user.player.item_set.get(data=knife_data)
        return_dict['desc_text'] = knife.data.desc_text
        return_dict['name'] = knife.data.name
        return_dict['img'] = knife.data.img_name
        if knife.is_examined:
            return_dict['exam_text'] = knife.data.exam_text
        elif knife.sent_away_time == None:
            return_dict['button'] = "Messer ins Labor schicken"

    elif name == "phone":
        phone_data = ItemMeta.objects.get(name="Handy")
        phone = request.user.player.item_set.get(data=phone_data)
        return_dict['desc_text'] = phone.data.desc_text
        return_dict['name'] = phone.data.name
        return_dict['img'] = phone.data.img_name
        if phone.is_examined:
            return_dict['exam_text'] = phone.data.exam_text
            return_dict['button'] = "Chats lesen"
            return_dict['button_id'] = "chats_button"
        elif phone.sent_away_time == None:
            return_dict['button'] = "Handy ins Labor schicken"

    elif name == "high_heels":
        heels_data = ItemMeta.objects.get(name="High Heels")
        heels = request.user.player.item_set.get(data=heels_data)
        return_dict['desc_text'] = heels.data.desc_text
        return_dict['name'] = heels.data.name
        return_dict['img'] = heels.data.img_name
        if heels.is_examined:
            return_dict['exam_text'] = heels.data.exam_text
        elif heels.sent_away_time == None:
            return_dict['button'] = "Schuhe ins Labor schicken"

    else:
        return_dict['error_message'] = "404 RESOURCE NOT FOUND"

    return HttpResponse(json.dumps(return_dict))

def items_send(request, name):
    player = request.user.player
    item = player.item_set.filter(data__name=name.replace("_", " "))[0]
    item.sent_away_time = timezone.now()
    item.is_visible = False
    item.save()
    return HttpResponse(json.dumps({'status':"OKAY"}))

def get_questions(request, personid):
    person = Person.objects.get(id=personid)

    if not person.questions_permitted(request.user.player):
        response_dict = {
            'type':'FORBIDDEN',
            'desc':'overflow'
        }
        return HttpResponse(json.dumps(response_dict))

    questions = person.available_questions(request.user.player)
    if isinstance(questions, dict) and questions['break'] != None:
        return HttpResponse(json.dumps(questions['return']))

    elif len(questions) == 1 and (questions[0].is_beginning or questions[0].text == "Anfangssatz 2"):
        response_dict = {
            'type':'BEGINNING',
            'person':personid,
            'video_title':questions[0].video_title
        }
        if hasattr(questions[0], "questioninterrupt"):
            response_dict['INTERRUPT'] = {}
            response_dict['INTERRUPT']['stop_time'] = questions[0].questioninterrupt.stop_time
            response_dict['INTERRUPT']['resume_time'] = questions[0].questioninterrupt.resume_time
            response_dict['INTERRUPT']['inspector'] = {}
            response_dict['INTERRUPT']['inspector']['title'] = questions[0].questioninterrupt.inspector_text.title
            response_dict['INTERRUPT']['inspector']['text'] = questions[0].questioninterrupt.inspector_text.text
            if questions[0].questioninterrupt.inspector_text.HTMLInput == "button":
                response_dict['INTERRUPT']['inspector']['button'] = True
                response_dict['INTERRUPT']['inspector']['value'] = questions[0].questioninterrupt.inspector_text.ButtonValue
        if person.name == "Mister Stripper":
            event_checker.cause_event(Event.objects.get(desc="Stripper_Question"), request.user.player)
        if questions[0].text == "Anfangssatz 2":
            event_checker.finish_event(Event.objects.get(desc="Stripper_Unlocked"), request.user.player)
        return HttpResponse(json.dumps(response_dict))

    response_dict = {
            'type':'QUESTIONS',
            'status':'OKAY',
            'person':personid,
            'questions': []
    }

    for question in questions: #interrupts müssen auch hier rein
        question_dict = {'id':question.id, 'text':question.text}
        if len(response_dict['questions']) < 7:
            response_dict['questions'].append(question_dict)
    return HttpResponse(json.dumps(response_dict))


def ask_question(request, questionid):
    question = Question.objects.get(id=questionid)
    asked_question = AskedQuestion(player=request.user.player, question=question, time=datetime.now())
    asked_question.save()
    if question.causes_event != None:
        event_checker.cause_event(question.causes_event, request.user.player)
    if len(request.user.player.asked_questions()) == 65:
        event_checker.cause_event(Event.objects.get(desc="Almost_Finished"), request.user.player)

    response_dict = {
            'type':'VIDEO',
            'video_title':question.video_title,
            'person':question.person.id,
            'follow_up': []
            }

    if hasattr(question, "questioninterrupt"):
        response_dict['INTERRUPT'] = {}
        response_dict['INTERRUPT']['stop_time'] = question.questioninterrupt.stop_time
        response_dict['INTERRUPT']['resume_time'] = question.questioninterrupt.resume_time
        response_dict['INTERRUPT']['inspector'] = {}
        response_dict['INTERRUPT']['inspector']['title'] = question.questioninterrupt.inspector_text.title
        response_dict['INTERRUPT']['inspector']['text'] = question.questioninterrupt.inspector_text.text
        if question.questioninterrupt.inspector_text.HTMLInput == "button":
            response_dict['INTERRUPT']['inspector']['button'] = True
            response_dict['INTERRUPT']['inspector']['value'] = question.questioninterrupt.inspector_text.ButtonValue


    if question.person.questions_permitted(request.user.player):
        if question.has_children():
            for child in question.child_questions.all():
                response_dict['follow_up'].append({'id':child.id, 'text':child.text})
        elif question.is_child():
            for child in question.parentquestion.child_questions.all():
                if not child.was_asked(request.user.player):
                    response_dict['follow_up'].append({'id':child.id, 'text':child.text})
        else:
            for question in question.person.available_questions(request.user.player):
                response_dict['follow_up'].append({'id':question.id, 'text':question.text})
    return HttpResponse(json.dumps(response_dict))


def confirm_beginning(request, personid):
    person = Person.objects.get(id=personid)
    player = request.user.player
    anfangssatz = person.question_set.filter(is_beginning=True)[0]
    asked = AskedQuestion(player = request.user.player, question = anfangssatz, time=datetime.now())
    asked.save()
    if person.id == 1:
        player.met_felix = True
    elif person.id == 5:
        player.met_sophia = True
    elif person.id == 6:
        player.met_julian = True
    elif person.id == 7:
        player.met_stripper = True
    elif person.id == 8:
        player.met_honey = True
    player.save()
    return HttpResponse(json.dumps({'status':'OKAY'}))


def check_events(request, page):
    player = request.user.player
    print(player.causedevent_set.all())
    if not player.causedevent_set.filter(finished=False):
        return HttpResponse(json.dumps({'status':'OKAY'}))

    return_list = []
    for event in player.causedevent_set.filter(finished=False):
        return_list.append(event_checker.check(event.event, page, request))

    if len(return_list) > 0:
        return HttpResponse(json.dumps(return_list))

    return HttpResponse(json.dumps({'status':'NOTHING'}))

def inspector_submit(request, submit_id, value):
    i = IntermediateStand(submit_id = submit_id, player = request.user.player, value=value, time=timezone.now())
    i.save()
    if submit_id == "stripper_question":
        e = Event.objects.get(desc="Stripper_Unlocked")
        if not e in request.user.player.caused_events():
            if value.lower().strip() in ["crystal", "cristal", "kristal", "krystal", "crystall", "cristall", "kristall", "krystall"]:
                event_checker.cause_event(e, request.user.player)
                return get_questions(request, 7)
            else:
                return HttpResponse(json.dumps({'status':'FAILURE', 'type':'INSPECTOR', 'insp':{'title':'Falsch...', 'text':'Scheint nicht so, als wäre das der richtige Name... Schade... Lass uns einfach später wiederkommen.'}}))

    return HttpResponse(json.dumps({'status':'OKAY'}))

def approve_chat(request, name):
    if name == "felix":
        return HttpResponse(json.dumps({'status':'OKAY'}))
    elif name == "julian":
        e = Event.objects.get(desc="Julian_Chat")
    elif name == "sophia":
        e = Event.objects.get(desc="Sophia_Chat")
    else:
        e = Event.objects.get(desc="Stripper_Chat")

    if e != None:
        event_checker.cause_event(e, request.user.player)
        return HttpResponse(json.dumps({'status':'OKAY'}))
    else:
        return HttpResponse("FAILURE")
