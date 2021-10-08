from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Player)

admin.site.register(Item)

admin.site.register(ItemMeta)
admin.site.register(Person)
admin.site.register(Place)

admin.site.register(Question)
admin.site.register(QuestionInterrupt)
admin.site.register(AskedQuestion)

admin.site.register(Event)
admin.site.register(CausedEvent)

admin.site.register(InspectorText)

admin.site.register(IntermediateStand)
