from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=300)
    def __str__(self):
        return self.question_text
class Game(models.Model):
    round_one_questions = models.ManyToManyField(Question, default=[],related_name='r_one')
    round_two_questions = models.ManyToManyField(Question, default=[], related_name = 'r_two')
    round_three_questions = models.ManyToManyField(Question,default=[],related_name='r_three')
    round_number = models.IntegerField(default=1)
    name = models.CharField(max_length=30)
    host = models.IntegerField(default=-1)
    num_players = models.IntegerField(default=0)
    def __str__(self):
        return self.name
class Player(models.Model):
    score = models.IntegerField()#eventually add choices
    name = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete = models.CASCADE)
    def __str__(self):
        return self.name
class Answer(models.Model):
    answer_text = models.CharField(max_length=100)
    player = models.ForeignKey(Player, on_delete = models.CASCADE)
    question = models.ForeignKey(Question, on_delete = models.CASCADE,default=1)
    def __str__(self):
        return self.answer_text

