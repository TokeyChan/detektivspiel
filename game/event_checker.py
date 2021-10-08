
from datetime import datetime, timedelta
from django.utils import timezone
from .models import InspectorText, Event, CausedEvent

def check(event, page, request):
    return_dict = {}


    if hasattr(event, "causes_inspector"):
        inspector = event.causes_inspector
        if page == inspector.page:
            if "{name}" in inspector.text:
                text = inspector.text.replace("{name}", request.user.username.capitalize())
            else:
                text = inspector.text
            inspector_list = [{'title':inspector.title, 'text':text}]

            if inspector.causes_event != None:
                cause_event(inspector.causes_event, request.user.player)
            if inspector.finishes_event != None:
                finish_event(inspector.finishes_event, request.user.player)

            if inspector.HTMLInput != None:
                if inspector.HTMLInput == "button":
                    inspector_list[0]['button'] = True
                elif inspector.HTMLInput == "input":
                    inspector_list[0]['input'] = True
                    inspector_list[0]['submitid'] = inspector.submit_id
                else:
                    inspector_list[0]['button'] = True
                    inspector_list[0]['input'] = True
                    inspector_list[0]['submitid'] = inspector.submit_id

                if inspector.ButtonValue != None:
                    inspector_list[0]['value'] = inspector.ButtonValue

            insp = inspector
            while insp.has_child():
                insp = insp.child
                insp_dict = {'title':insp.title, 'text':insp.text}
                if insp.HTMLInput != None:
                    if insp.HTMLInput == "button":
                        insp_dict['button'] = True
                    elif insp.HTMLInput == "input":
                        insp_dict['input'] = True
                        insp_dict['submitid'] = insp.submit_id
                    else:
                        insp_dict['button'] = True
                        insp_dict['input'] = True
                        insp_dict['submitid'] = insp.submit_id
                    if insp.ButtonValue != None:
                        insp_dict['value'] = insp.ButtonValue

                inspector_list.append(insp_dict)
                if insp.causes_event != None:
                    cause_event(insp.causes_event, request.user.player)
                if insp.finishes_event != None:
                    finish_event(insp.finishes_event, request.user.player)

            return_dict['inspector'] = inspector_list


    if event.desc == "Sophia_Eifersucht" or event.desc == "Sophia_Chat":
        if Event.objects.get(desc="Sophia_Eifersucht") in request.user.player.caused_events() and Event.objects.get(desc="Sophia_Chat") in request.user.player.caused_events():
            cause_event(Event.objects.get(desc="Eifersucht_and_Phone"), request.user.player)



    if len(return_dict.keys()) > 0:
        return_dict['status'] = "EXECUTE"
    else:
        return_dict['status'] = "OKAY"
    return return_dict


def cause_event(event, player):
    if event in player.caused_events():
        return
    e = CausedEvent(event=event, player=player, time=timezone.now(), finished=event.auto_finished())
    e.save()
    if event.desc == "Tutorial_Finished":
        player.cafe_visitable = True
    elif event.desc == "Felix:Julian":
        player.park_visitable = True
    elif event.desc == "Felix:Laden":
        player.old_but_gold_visitable = True
    elif event.desc == "Stripper_Chat":
        player.twoinone_visitable = True
    elif event.desc == "Sophia_Eifersucht" or event.desc == "Sophia_Chat":
        #print("Haaaaaaaaaaa")
        if Event.objects.get(desc="Sophia_Eifersucht") in player.caused_events() and Event.objects.get(desc="Sophia_Chat") in player.caused_events():
            e = CausedEvent(event=Event.objects.get(desc="Eifersucht_and_Phone"), player=player, time=timezone.now(), finished=event.auto_finished())
            e.save()


    player.save()

def finish_event(event, player):
    e = player.causedevent_set.get(event=event)
    e.finished = True
    e.save()


item_event = Event.objects.get(desc="Items_Returned")
def check_items(player):
    for item in player.item_set.all():
        if item.sent_away_time != None:
            if item.sent_away_time + timedelta(minutes=20) < timezone.now():
                item.is_examined = True
                item.is_visible = True
                item.save()
                if not item_event in player.caused_events():
                    ce = CausedEvent(player=player, event=item_event, time=datetime.now(), finished=item_event.auto_finished())
                    ce.save()
