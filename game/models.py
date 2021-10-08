from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import timedelta



class Place(models.Model):
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100, default="")
    html_id = models.CharField(max_length=100)
    background_img = models.CharField(max_length=100, null=True, blank=True)
    visitable_by_default = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name


class Person(models.Model):
    name = models.CharField(max_length=100)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    is_suspect = models.BooleanField(default=True)

    def __str__(self):
        return f"({self.id}){self.name}"

    def available_questions(self, player):
        anfangssatz = self.question_set.get(is_beginning=True)
        asked_questions = player.asked_questions()

        if not anfangssatz in asked_questions:
            return [anfangssatz]

        if self.name == "Mister Stripper":
            e = Event.objects.get(desc="Stripper_Unlocked")
            if not e in player.caused_events():
                insp = InspectorText.objects.get(title="Name?")
                dict = {'break':True, 'return':{'type':'INSPECTOR', 'insp':{
                    'title':insp.title,
                    'text':insp.text}}}
                if insp.HTMLInput != None:
                    if insp.HTMLInput == "button":
                        dict['return']['insp']['button'] = True
                    elif insp.HTMLInput == "input":
                        dict['return']['insp']['input'] = True
                        dict['return']['insp']['submitid'] = insp.submit_id
                    else:
                        dict['return']['insp']['button'] = True
                        dict['return']['insp']['input'] = True
                        dict['return']['insp']['submitid'] = insp.submit_id
                    if insp.ButtonValue != None:
                        dict['return']['insp']['value'] = insp.ButtonValue
                ce = Event.objects.get(desc="Stripper_Question")
                finish_event(ce, player)
                return dict
            elif not player.causedevent_set.get(event=e).finished:
                return [self.question_set.get(text="Anfangssatz 2")]

        questions = self.question_set.all()
        unasked_questions = []

        for question in questions:
            if not question in asked_questions:
                if question.gets_unlocked:
                    try:
                        if player.causedevent_set.get(event=question.on_event):
                            unasked_questions.append(question)
                    except:
                        print("not found")
                elif not question.is_child():
                    unasked_questions.append(question)
                elif question.parentquestion in asked_questions: #if child
                    unasked_questions.append(question)
        return unasked_questions



    def questions_permitted(self, player):
        asked_questions = player.askedquestion_set.all()
        counter = 0

        for question in asked_questions:
            if question.question.person == self and question.was_asked_recently():
                counter += 1

        if self.name == "Mister Stripper":
            if counter > 6:
                return False
            else:
                return True
        elif counter > 4:
            return False
        else:
            return True

class Event(models.Model):
    desc = models.CharField(max_length=200)

    def __str__(self):
        return self.desc

    def auto_finished(self):
        if self.desc == "Stripper_Unlocked":
            return False
        return False if hasattr(self, "causes_inspector") else True

class CausedEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    time = models.DateTimeField(null=True, blank=True)
    finished = models.BooleanField(default=False)
    #finished soll automatisch True sein, wenn das Event nur Fragen auslöst und sonst nix.

    def __str__(self):
        return f"({self.player.user.username})-{self.event.desc}"

class Question(models.Model):
    text = models.CharField(max_length=100, blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    gets_unlocked = models.BooleanField(default=False)
    is_beginning = models.BooleanField(default=False)
    video_title = models.CharField(max_length=100, blank=True)
    parentquestion = models.ForeignKey("self", related_name="child_questions", on_delete=models.CASCADE, blank=True, null=True)
    causes_event = models.OneToOneField(Event, related_name="caused_by_question", on_delete=models.CASCADE, blank=True, null=True)
    on_event = models.ForeignKey(Event, related_name="causes_questions", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"({self.id})-[{self.person.name}]-{self.text[:30]}"

    def is_child(self):
        if self.parentquestion != None:
            return True
        else:
            return False

    def has_children(self):
        if len(self.child_questions.all()) > 0:
            return True
        else:
            return False

    def was_asked(self, player):
        if self in player.asked_questions():
            return True
        else:
            return False

class AskedQuestion(models.Model):
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.player.user.username}_[{self.question.person.name}]_{self.question.text[:30]}"
    def was_asked_recently(self):
        return self.time >= timezone.now() - timedelta(minutes=10)

class QuestionInterrupt(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    stop_time = models.FloatField()
    resume_time = models.FloatField()
    inspector_text = models.OneToOneField("InspectorText", on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=30, null=True, blank=True)

class InspectorText(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=600)
    causes_event = models.OneToOneField(Event, related_name="caused_by_inspector", on_delete=models.CASCADE, blank=True, null=True)
    on_event = models.OneToOneField(Event, related_name="causes_inspector", on_delete=models.CASCADE, blank=True, null=True)
    parenttext = models.OneToOneField("self", related_name="child", on_delete=models.CASCADE, blank=True, null=True)
    page = models.CharField(max_length=100, blank=True, null=True)
    finishes_event = models.ForeignKey(Event, related_name="finished_by_inspector", on_delete=models.CASCADE, blank=True, null=True)
    HTMLInput = models.CharField(max_length=20, blank=True, null=True)
    ButtonValue = models.CharField(max_length=20, blank=True, null=True)
    submit_id = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title + (" nach: " + self.parenttext.title if self.has_parent() else "")

    def has_parent(self):
        return self.parenttext != None

    def has_child(self):
        return hasattr(self, "child")

class ItemMeta(models.Model):
    name = models.CharField(max_length=100)
    desc_text = models.CharField(max_length=500)
    exam_text = models.CharField(max_length=500)
    img_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Item(models.Model):
    is_visible = models.BooleanField(default=True)
    is_examined = models.BooleanField(default=False)
    sent_away_time = models.DateTimeField(null=True, blank=True)
    data = models.ForeignKey(
        ItemMeta,
        on_delete = models.CASCADE
    )
    player = models.ForeignKey(
        "Player",
        on_delete = models.CASCADE
    )
    def __str__(self):
        return self.data.name + " " + self.player.user.username

class IntermediateStand(models.Model):
    submit_id = models.CharField(max_length=25)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    value = models.CharField(max_length=25)
    time = models.DateTimeField()

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    park_visitable = models.BooleanField(default=False)
    old_but_gold_visitable = models.BooleanField(default=False)
    twoinone_visitable = models.BooleanField(default=False)
    cafe_visitable = models.BooleanField(default=False)

    met_felix = models.BooleanField(default=False)
    met_julian = models.BooleanField(default=False)
    met_sophia = models.BooleanField(default=False)
    met_honey = models.BooleanField(default=False)
    met_stripper = models.BooleanField(default=False)

    final_score = models.IntegerField(null=True, blank=True)

    #caused_events = models.ForeignKey(CausedEvent, on_delete=models.CASCADE, blank=True, null=True)
    #asked_questions = models.CharField(max_length=500, null=True)
    def __str__(self):
        return self.user.username

    def asked_questions(self):
        return [q.question for q in self.askedquestion_set.all()]

    def caused_events(self):
        return [e.event for e in self.causedevent_set.all()]

    def has_finished(self):
        return True if self.final_score is not None else False

def finish_event(event, player):
    e = player.causedevent_set.get(event=event)
    e.finished = True
    e.save()
