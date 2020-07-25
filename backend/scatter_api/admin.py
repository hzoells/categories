from django.contrib import admin
from .models import Question, Answer, Game, Player
# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Game)
admin.site.register(Player)
